import re
from typing import Union

import bs4

from TvFY.collector.helpers import SoupSelectionMixin
from TvFY.movies.models import Movie


class IMDBEpisodes(SoupSelectionMixin):
    url: str

    @staticmethod
    def get_imdb_vote_count(episode_data):
        vote_str = episode_data.find('span', class_='ipl-rating-star__total-votes').text
        vote_count = int("".join(re.findall(r'\d+', vote_str)))
        return vote_count

    @property
    def get_episodes(self) -> dict:
        result = []
        css_selection = self.soup_selection(
            self.find_all, selection="info", tag="div"
        )
        for episode_data in css_selection:
            data = {
                "name": episode_data.a['title'],
                "storyline": episode_data.find(
                    'div', class_='item_description').text.strip(),
                "imdb_rate": episode_data.find(
                    'span', class_='ipl-rating-star__rating').text,
                "imdb_vote_count": self.get_imdb_vote_count(episode_data),
                "episode": episode_data.meta['content'],
                "release_date": episode_data.find('div', class_='airdate').text.strip(),
                "season": self.url
            }
            result.append(data)
        return {"episodes": result}


class IMDBCast(SoupSelectionMixin):
    search_type: str

    @staticmethod
    def get_actor_name(cast_data: str) -> dict:
        first_name, *last_name = cast_data.split(" ")
        result = {"first_name": first_name, "last_name": " ".join(last_name)}
        return result

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
        years = year.split("-")
        result = {
            "character_name": character_name,
            "episode_count": episode_count,
            "start_acting": years[0],
            "end_acting": years[~0]
        }
        return result

    @property
    def get_cast(self) -> dict:
        results = []
        css_selection = self.soup_selection(
            self.find, selection="cast_list", tag="table"
        )
        for cast in css_selection.find_all("tr"):
            if character := cast.find('td', class_="character"):
                if self.search_type == Movie.type:
                    cast_information = {"character_name": character.a.text}
                else:
                    cast_information = self.cast_information(character.get_text(" sp "))
                if not cast_information:
                    continue

                actor = self.get_actor_name(cast.find("td", class_="").a.text.strip())
                actor.update(cast_information)
                results.append(actor)
        return {"cast": results}


class IMDBAwards(SoupSelectionMixin):
    @property
    def get_awards(self) -> dict:
        css_selection = self.soup_selection(
            self.find, selection="desc", tag="div"
        )
        if text := css_selection.text:
            wins, nominations = re.findall(r'\d+', text)
        else:
            wins, nominations = 0, 0

        return {"wins": wins, "nominations": nominations}


class IMDBScrapper(IMDBEpisodes, IMDBCast, IMDBAwards):
    def __init__(self, soup: bs4, url: str, search_type: str):
        self.soup = soup
        self.url = url
        self.search_type = search_type

    @property
    def get_popularity(self) -> dict:
        css_selection = self.soup_selection(
            self.find, selection="titleReviewBarSubItem", tag="div"
        )
        popularity = css_selection.span.text.split("(")
        return {"popularity": popularity[0].strip()}

    @property
    def get_creator(self) -> dict:
        css_selection = self.soup_selection(
            self.find, selection="credit_summary_item", tag="div"
        )
        return {"creator": css_selection.a.text.strip()}

    @property
    def get_genre(self) -> dict:
        genres = None
        css_selection = self.soup_selection(
            self.select_one, selection="#titleStoryLine"
        )
        for data in css_selection.find_all("div", class_="see-more inline canwrap"):
            if data.h4 and data.h4.text == 'Genres:':
                genres = {
                    "genres_imdb": [genre.text.strip() for genre in data.find_all('a')]
                }
        return genres

    @property
    def get_runtime(self) -> dict:
        css_selection = self.soup_selection(
            self.find, tag="time"
        )
        return {"run_time": css_selection.text.strip()}

    @staticmethod
    def get_language(content) -> dict:
        language = None
        if content.h4 and content.h4.text == 'Language:':
            language = {"language": [a.text for a in content.find_all("a")]}
        return language

    @staticmethod
    def get_country(content: bs4) -> dict:
        country = None
        if content.h4 and content.h4.text == 'Country:':
            country = {"country": [a.text for a in content.find_all("a")]}
        return country

    @staticmethod
    def get_budget(content: bs4) -> dict:
        budget = None
        if content.h4 and content.h4.text == 'Budget:':
            content = content.get_text(" sp ")
            # ['\n', 'Budget:', '$93,000,000\n', '(estimated)', '\n']
            gross = content.split(" sp ")[2].strip()
            budget = {"budget": re.sub('[$,]', '', gross)}
        return budget

    @staticmethod
    def get_usa_opening_weekend(content: bs4) -> dict:
        usa_opening_weekend = None
        if content.h4 and content.h4.text == 'Opening Weekend USA:':
            content = content.get_text(" sp ")
            # ['\n', 'Opening Weekend USA:', ' $47,211,490,\n', '23 December 2001', ' ']
            gross = content.split(" sp ")[2].strip()
            usa_opening_weekend = {"usa_opening_weekend": re.sub('[$,]', '', gross)}
        return usa_opening_weekend

    @staticmethod
    def get_ww_gross(content: bs4) -> dict:
        ww_gross = None
        if content.h4 and content.h4.text == 'Cumulative Worldwide Gross:':
            content = content.get_text(" sp ")
            # ['\n', 'Cumulative Worldwide Gross:', '$888,159,092']
            gross = content.split(" sp ")[2].strip()
            ww_gross = {"ww_gross": re.sub('[$,]', '', gross)}
        return ww_gross

    def run_method(self, action: str, content: str):
        action_class: dict = {
            "get_country": self.get_country,
            "get_language": self.get_language,
            "get_budget": self.get_budget,
            "get_usa_opening_weekend": self.get_usa_opening_weekend,
            "get_ww_gross": self.get_ww_gross,
        }
        action_method: classmethod = action_class[action]
        return action_method(content=content)

    @property
    def split_details(self) -> dict:
        """
        Get data under title details.
        """
        result = {}
        actions = ["get_country", "get_language"]
        if self.search_type == Movie.type:
            actions.extend(
                ["get_budget", "get_usa_opening_weekend", "get_ww_gross"]
            )
        css_selection = self.soup_selection(
            self.select_one, selection="#titleDetails"
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
        if 'episodes' in self.url:
            result.update(self.get_episodes)
        elif 'fullcredits' in self.url:
            result.update(self.get_cast)
        elif 'awards' in self.url:
            result.update(self.get_awards)
        else:
            result.update(self.split_details)
            result.update(self.get_popularity)
            result.update(self.get_creator)
            result.update(self.get_genre)
            result.update(self.get_runtime)
        return result
