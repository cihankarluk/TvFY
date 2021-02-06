import re
import urllib.parse as urlparse
from datetime import datetime
from typing import Union
from urllib.parse import parse_qs

import bs4

from TvFY.collector.helpers import SoupSelectionMixin
from TvFY.core.helpers import get_date_time
from TvFY.movies.models import Movie


class IMDBEpisodes(SoupSelectionMixin):
    url: str

    def get_imdb_vote_count(self, episode_data: bs4) -> int:
        vote_str = self.soup_selection(
            soup=episode_data,
            method="find",
            tag="span",
            class_="ipl-rating-star__total-votes",
        ).text
        vote_count = int("".join(re.findall(r"\d+", vote_str)))
        return vote_count

    @property
    def get_season(self) -> int:
        parsed = urlparse.urlparse(self.url)
        season: str = parse_qs(parsed.query)["season"][0]
        return int(season)

    @property
    def get_episodes(self) -> dict:
        result = []
        css_selection = self.soup_selection(
            soup=self.soup, method=self.find_all, tag="div", class_="info"
        )
        for episode_data in css_selection:
            date = self.soup_selection(
                soup=episode_data, method="find", tag="div", class_="airdate"
            ).text.strip()
            data = {
                "name": episode_data.a["title"],
                "storyline": episode_data.find(
                    "div", class_="item_description"
                ).text.strip(),
                "imdb_rate": float(
                    episode_data.find("span", class_="ipl-rating-star__rating").text
                ),
                "imdb_vote_count": self.get_imdb_vote_count(episode_data),
                "episode": int(episode_data.meta["content"]),
                "release_date": get_date_time(date, "%d %b. %Y"),
                "imdb_url": self.url,
            }
            result.append(data)
        return {self.get_season: result}


class IMDBCast(SoupSelectionMixin):
    search_type: str

    @staticmethod
    def cast_information(cast_data: str) -> Union[bool, dict]:
        # info: '17 episodes, 2019-2022'
        cast_data_list = cast_data.split(" sp ")

        character_name = cast_data_list[1].strip()
        # 17, episodes, 2019-2022
        character_detail = cast_data_list[3].strip()
        try:
            episode_count, _, year = character_detail.split(" ")
        except ValueError:
            # 'unknown episodes'
            episode_count = False

        if not episode_count:
            # Case for dummy data
            return False

        # years 2019 or 2019-2022
        years = year.split("-")  # noqa
        result = {
            "character_name": character_name,
            "episode_count": int(episode_count),
            "start_acting": datetime.strptime(years[0], "%Y"),
            "end_acting": datetime.strptime(years[~0], "%Y"),
        }
        return result

    @property
    def get_cast(self) -> dict:
        results = []
        css_selection = self.soup_selection(
            soup=self.soup, method=self.find, tag="table", class_="cast_list"
        )
        for cast in css_selection.find_all("tr"):
            if character := cast.find("td", class_="character"):
                if self.search_type == Movie.TYPE:
                    cast_information = {"character_name": character.a.text}
                else:
                    cast_information = self.cast_information(character.get_text(" sp "))
                if not cast_information:
                    continue
                actor = self.get_name(cast.find("td", class_="").a.text.strip())
                actor.update(cast_information)
                results.append(actor)

        return {"cast": results}


class IMDBAwards(SoupSelectionMixin):
    @property
    def get_awards(self) -> dict:
        css_selection = self.soup_selection(
            soup=self.soup, method=self.find, tag="div", class_="desc"
        )
        if text := css_selection.text:
            wins, nominations = re.findall(r"\d+", text)
        else:
            wins, nominations = 0, 0

        return {"wins": int(wins), "nominations": int(nominations)}


class IMDBMovie(SoupSelectionMixin):
    @staticmethod
    def get_budget(content: bs4) -> dict:
        budget = {}
        if content.h4 and content.h4.text == "Budget:":
            content = content.get_text(" sp ")
            # ['\n', 'Budget:', '$93,000,000\n', '(estimated)', '\n']
            gross = content.split(" sp ")[2].strip()
            budget = {"budget": re.sub("[$,]", "", gross)}
        return budget

    @staticmethod
    def get_usa_opening_weekend(content: bs4) -> dict:
        usa_opening_weekend = {}
        if content.h4 and content.h4.text == "Opening Weekend USA:":
            content = content.get_text(" sp ")
            # TODO: need to add currency control
            # ['\n', 'Opening Weekend USA:', ' $47,211,490,\n', '23 December 2001', ' ']
            gross = content.split(" sp ")[2].strip()
            usa_opening_weekend = {"usa_opening_weekend": re.sub("[$,]", "", gross)}
        return usa_opening_weekend

    @staticmethod
    def get_ww_gross(content: bs4) -> dict:
        ww_gross = {}
        if content.h4 and content.h4.text == "Cumulative Worldwide Gross:":
            content = content.get_text(" sp ")
            # ['\n', 'Cumulative Worldwide Gross:', '$888,159,092']
            gross = content.split(" sp ")[2].strip()
            ww_gross = {"ww_gross": re.sub("[$,]", "", gross)}
        return ww_gross


class IMDBScrapper(IMDBEpisodes, IMDBCast, IMDBAwards, IMDBMovie):
    episodes = "episodes"
    fullcredits = "fullcredits"
    awards = "awards"

    def __init__(self, soup: bs4, url: str, search_type: str):
        self.soup = soup
        self.url = url
        self.search_type = search_type

    @property
    def get_genre(self) -> dict:
        genres = {}
        css_selection = self.soup_selection(
            soup=self.soup, method=self.select_one, selector="#titleStoryLine"
        )
        for data in css_selection.find_all("div", class_="see-more inline canwrap"):
            if data.h4 and data.h4.text == "Genres:":
                genres = {
                    "imdb_genre": [genre.text.strip() for genre in data.find_all("a")]
                }
        return genres

    @property
    def get_creator(self) -> dict:
        css_selection = self.soup_selection(
            soup=self.soup, method=self.find, tag="div", class_="credit_summary_item"
        )
        return {"creator": css_selection.a.text.strip()}

    @property
    def get_total_vote_count(self):
        css_selection = self.soup_selection(
            soup=self.soup,
            method="find",
            tag="span",
            class_="small",
            itemprop="ratingCount",
        )
        vote_count = css_selection.text.replace(",", "")
        return {"total_imdb_vote_count": int(vote_count)}

    @property
    def get_total_imdb_rating(self):
        css_selection = self.soup_selection(
            soup=self.soup, method="find", tag="span", itemprop="ratingValue"
        )
        return {"total_imdb_rate": float(css_selection.text)}

    @property
    def get_runtime(self) -> dict:
        css_selection = self.soup_selection(
            soup=self.soup, method=self.find, tag="time"
        )
        # '2h 58min' or '1h' or '24min'
        run_time_list = css_selection.text.strip().split("h")
        if len(run_time_list) > 1:
            hour = int(run_time_list[0]) * 60
            if minute := run_time_list[-1].strip("min"):
                minute = int(minute)
            run_time = hour + (minute or 0)
        elif run_time_list[0]:
            run_time = int(run_time_list[0].strip("min"))
        else:
            run_time = 0
        return {"run_time": run_time}

    @property
    def get_popularity(self) -> dict:
        css_selection = self.soup_selection(
            soup=self.soup, method=self.find, tag="div", class_="titleReviewBarSubItem"
        )
        popularity = css_selection.span.text.split("(")
        return {"popularity": popularity[0].strip()}

    @staticmethod
    def get_country(content: bs4) -> dict:
        country = {}
        if content.h4 and content.h4.text == "Country:":
            country = {"country": [a.text for a in content.find_all("a")]}
        return country

    @staticmethod
    def get_language(content) -> dict:
        language = {}
        if content.h4 and content.h4.text == "Language:":
            language = {"language": [a.text for a in content.find_all("a")]}
        return language

    @staticmethod
    def get_release_date(content) -> dict:
        release_date = {}
        if content.h4 and content.h4.text == "Release Date:":
            text = content.get_text(" sp ")
            date = text.split(" sp ")[2].strip().split(" (")[0]
            release_date = {"release_date": get_date_time(date, "%d %B %Y")}
        return release_date

    @property
    def get_title(self):
        css_selection = self.soup_selection(
            soup=self.soup, method=self.find, tag="div", class_="title_wrapper"
        )
        if title := css_selection.h1:
            title = title.text.strip()
        return {"title": title}

    @property
    def get_is_active(self) -> dict:
        is_active = False
        css_selection = self.soup_selection(
            soup=self.soup, method="find", tag="a", title="See more release dates"
        )
        text = css_selection.text.strip()
        if re.search(r"\d{4}–\s", text):
            is_active = True
        return {"is_active": is_active}

    def run_method(self, action: str, content: str):
        action_class: dict = {
            "get_country": self.get_country,
            "get_language": self.get_language,
            "get_release_date": self.get_release_date,
            "get_budget": self.get_budget,
            "get_usa_opening_weekend": self.get_usa_opening_weekend,
            "get_ww_gross": self.get_ww_gross,
        }
        action_method: classmethod = action_class[action]
        return action_method(content=content)

    def split_details(self, actions) -> dict:
        """
        Get data under title details.
        """
        result = {}
        css_selection = self.soup_selection(
            soup=self.soup, method=self.select_one, selector="#titleDetails"
        )
        for div in css_selection.find_all("div"):
            for index, action in enumerate(actions):
                if data := self.run_method(action, div):
                    actions.pop(index)
                    result.update(data)
            if not actions:
                break
        return result

    def run(self):
        result = {}
        actions = ["get_country", "get_language", "get_release_date"]
        if self.episodes in self.url:
            result.update(self.get_episodes)
        elif self.fullcredits in self.url:
            result.update(self.get_cast)
        elif self.awards in self.url:
            result.update(self.get_awards)
        elif self.search_type == Movie.TYPE:
            actions.extend(["get_budget", "get_usa_opening_weekend", "get_ww_gross"])
            result.update(self.split_details(actions=actions))
            result.update(self.get_genre)
            result.update(self.get_title)
            result.update(self.get_creator)
            result.update(self.get_runtime)
            result.update(self.get_popularity)
            result.update(self.get_total_vote_count)
            result.update(self.get_total_imdb_rating)
        else:
            result.update(self.split_details(actions=actions))
            result.update(self.get_genre)
            result.update(self.get_title)
            result.update(self.get_creator)
            result.update(self.get_runtime)
            result.update(self.get_popularity)
            result.update(self.get_total_vote_count)
            result.update(self.get_total_imdb_rating)
            result.update(self.get_is_active)
        return result
