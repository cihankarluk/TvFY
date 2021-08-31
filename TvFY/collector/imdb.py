import re
import urllib.parse as urlparse
from collections import defaultdict
from datetime import datetime
from typing import Union
from urllib.parse import parse_qs

from bs4 import BeautifulSoup

from TvFY.collector.helpers import SoupSelectionMixin
from TvFY.core.helpers import get_date_time, regex_search
from TvFY.movies.models import Movie
from TvFY.series.models import Series


class IMDBEpisodes:
    url: str
    find: str
    find_all: str
    soup_selection: classmethod
    soup: BeautifulSoup

    def get_imdb_vote_count(self, episode_data: BeautifulSoup) -> int:
        vote_count = 0

        soup_selection = {
            "soup": episode_data,
            "method": self.find,
            "tag": "span",
            "class": "ipl-rating-star__total-votes",
        }
        if css_selection := self.soup_selection(**soup_selection):
            vote_count = int("".join(re.findall(r"\d+", css_selection.text)))

        return vote_count

    @property
    def get_season(self) -> int:
        parsed = urlparse.urlparse(self.url)
        season: str = parse_qs(parsed.query)["season"][0]
        return int(season)

    def get_episode_release_date(self, episode_data):
        date = self.soup_selection(
            soup=episode_data, method="find", tag="div", class_="airdate"
        ).text.strip()
        try:
            date_time = get_date_time(date, "%d %b. %Y")
        except ValueError:
            date_time = get_date_time(date, "%d %b %Y")
        return date_time

    @property
    def get_episodes(self) -> dict:
        episodes = {}

        soup_selection = {
            "soup": self.soup,
            "method": self.find_all,
            "tag": "div",
            "class": "info",
        }
        if css_selection := self.soup_selection(**soup_selection):
            result = []
            for episode_data in css_selection:
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
                    "release_date": self.get_episode_release_date(episode_data),
                    "imdb_url": self.url,
                }
                result.append(data)
            episodes = {self.get_season: result}

        return episodes


class IMDBCast:
    url: str
    find: str
    find_all: str
    soup_selection: classmethod
    get_name: classmethod
    soup: BeautifulSoup
    search_type: str

    @staticmethod
    def cast_information(cast_data: str) -> Union[bool, dict]:
        # info: '17 episodes, 2019-2022'
        cast_data_list = cast_data.split(" sp ")

        character_name = cast_data_list[1].strip()
        try:
            # 17, episodes, 2019-2022
            character_detail = cast_data_list[3].strip()
            episode_count, _, year = character_detail.split(" ")
        except (ValueError, IndexError):
            # 'unknown episodes' or unknown character_name
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
        cast = {}

        soup_selection = {
            "soup": self.soup,
            "method": self.find,
            "tag": "table",
            "class": "cast_list",
        }
        if css_selection := self.soup_selection(**soup_selection):
            results = []
            for cast in css_selection.find_all("tr"):
                if character := cast.find("td", class_="character"):
                    if self.search_type == Movie.TYPE:
                        cast_information = {"character_name": character.a.text}
                    else:
                        cast_information = self.cast_information(
                            character.get_text(" sp ")
                        )
                    if not cast_information:
                        continue

                    actor_detail = cast.find("td", class_="").a
                    actor = self.get_name(actor_detail.text.strip())
                    actor.update(cast_information)
                    actor.update({"imdb_actor_url": actor_detail["href"]})
                    results.append(actor)
            cast = {"cast": results}

        return cast


class IMDBAwards:
    url: str
    find: str
    soup_selection: classmethod
    soup: BeautifulSoup

    @property
    def get_awards(self) -> dict:
        awards = {}

        soup_selection = {
            "soup": self.soup,
            "method": self.find,
            "tag": "div",
            "class": "desc",
        }
        if css_selection := self.soup_selection(**soup_selection):
            wins, nominations = re.findall(r"\d+", css_selection.text)
            awards = {"wins": int(wins), "nominations": int(nominations)}

        return awards


class IMDBPersonalData:
    url: str
    find: str
    find_all: str
    soup_selection: classmethod
    soup: BeautifulSoup

    @property
    def get_birth_date(self) -> dict:
        born_date = {}

        soup_selection = {
            "soup": self.soup,
            "method": self.find,
            "tag": "div",
            "id": "name-born-info",
        }
        if css_selection := self.soup_selection(**soup_selection):
            born_date = {
                "born_date": datetime.strptime(
                    css_selection.time["datetime"], "%Y-%m-%d"
                )
            }

        return born_date

    @property
    def get_born_place(self) -> dict:
        born_at = {}

        soup_selection = {
            "soup": self.soup,
            "method": self.find,
            "tag": "div",
            "id": "name-born-info",
        }
        if css_selection := self.soup_selection(**soup_selection):
            born_at = {"born_at": css_selection.find_all("a")[-1].text}

        return born_at

    @property
    def get_death_date(self) -> dict:
        died_date = {"died_date": None}

        soup_selection = {
            "soup": self.soup,
            "method": self.find,
            "tag": "div",
            "id": "name-death-info",
        }
        if css_selection := self.soup_selection(**soup_selection):
            died_date = {
                "died_date": datetime.strptime(
                    css_selection.time["datetime"], "%Y-%m-%d"
                )
            }

        return died_date

    @property
    def get_death_place(self) -> dict:
        died_at = {"died_at": None}

        soup_selection = {
            "soup": self.soup,
            "method": self.find,
            "tag": "div",
            "id": "name-death-info",
        }
        if css_selection := self.soup_selection(**soup_selection):
            died_at = {"died_at": css_selection.find_all("a")[-1].text}

        return died_at

    @property
    def get_person_awards(self) -> dict:
        result = {"oscars": None, "oscar_nominations": None}

        soup_selection = {
            "soup": self.soup,
            "method": self.find_all,
            "tag": "span",
            "class": "awards-blurb",
        }
        if css_selection := self.soup_selection(**soup_selection):
            oscar_data = css_selection[0].get_text(strip=True)
            search = regex_search(oscar_data, r"\d{1,2}")
            if "Won" in oscar_data:
                result.update({"oscars": search})
            elif len(css_selection) > 1:
                # If there is no oscar wins and nominations
                result.update({"oscar_nominations": search})

            wins, nominations = re.findall(
                r"\d+", css_selection[-1].get_text(strip=True)
            )
            result.update({"wins": wins, "nominations": nominations})

        return result

    @property
    def get_perks(self) -> dict:
        perks = defaultdict(list)

        soup_selection = {
            "soup": self.soup,
            "method": self.find,
            "tag": "div",
            "class": "infobar",
        }
        if css_selection := self.soup_selection(**soup_selection):
            for perk in css_selection.find_all("a"):
                perk = perk["href"].replace("#", "")
                perks["perks"].append(perk)

        return perks


class IMDBRating:
    url: str
    find: str
    find_all: str
    soup_selection: classmethod
    soup: BeautifulSoup

    @property
    def get_total_vote(self) -> dict:
        total_imdb_vote = {}

        soup_selection = {
            "soup": self.soup,
            "method": self.find,
            "tag": "div",
            "class": "allText",
        }
        if css_selection := self.soup_selection(**soup_selection):
            selection_list = css_selection.get_text(strip=True).splitlines()
            # ['304,144', 'IMDb users have given aweighted averagevote of  8.7 / 10]
            total_imdb_vote = {
                "total_imdb_vote": int(selection_list[0].replace(",", ""))
            }

        return total_imdb_vote

    @property
    def get_average_rating(self) -> dict:
        average_imdb_rate = {}

        soup_selection = {
            "soup": self.soup,
            "method": self.find,
            "tag": "span",
            "class": "ipl-rating-star__rating",
        }
        if css_selection := self.soup_selection(**soup_selection):
            average_imdb_rate = {"average_imdb_rate": float(css_selection.text)}

        return average_imdb_rate


class IMDBHomePage:
    url: str
    find: str
    find_all: str
    soup_selection: classmethod
    soup: BeautifulSoup

    @property
    def get_genre(self) -> dict:
        genres = {}

        soup_selection = {
            "soup": self.soup,
            "method": self.find,
            "tag": "div",
            "data-testid": "genres",
        }
        if css_selection := self.soup_selection(**soup_selection):
            genres = {"imdb_genre": css_selection.get_text("-").split("-")}

        return genres

    @property
    def get_creator(self) -> dict:
        creator = {}

        soup_selection = {
            "soup": self.soup,
            "method": self.find,
            "tag": "div",
            "class": "credit_summary_item",
        }
        if css_selection := self.soup_selection(**soup_selection):
            creator = {
                "creator": css_selection.a.text.strip(),
                "imdb_creator_url": css_selection.a["href"],
            }

        return creator

    @property
    def get_director(self) -> dict:
        director = {}

        soup_selection = {
            "soup": self.soup,
            "method": self.find,
            "tag": "a",
            "class": "ipc-metadata-list-item__list-content-item ipc-metadata-list-item__list-content-item--link",  # NOQA: E501
        }
        if css_selection := self.soup_selection(**soup_selection):
            director = {
                "director": css_selection.text,
                "imdb_director_url": css_selection["href"],
            }

        return director

    @property
    def get_runtime(self) -> dict:
        runtime = {}

        soup_selection = {
            "soup": self.soup,
            "method": self.find,
            "tag": "ul",
            "data-testid": "hero-title-block__metadata",
        }
        if css_selection := self.soup_selection(**soup_selection):
            # '2h 58min' or '1h' or '24min'
            runtime_str = css_selection.get_text("~").split("~")[-1]
            runtime_int = self.convert_runtime(runtime_str)
            runtime = {"run_time": runtime_int}

        return runtime

    @property
    def get_popularity(self) -> dict:
        imdb_popularity = {}

        soup_selection = {
            "soup": self.soup,
            "method": self.find,
            "tag": "div",
            "data-testid": "hero-rating-bar__popularity__score",
        }
        if css_selection := self.soup_selection(**soup_selection):
            imdb_popularity = {"imdb_popularity": css_selection.text}

        return imdb_popularity

    @property
    def get_country(self) -> dict:
        country = {}

        soup_selection = {
            "soup": self.soup,
            "method": self.find,
            "tag": "li",
            "data-testid": "title-details-origin",
        }
        if css_selection := self.soup_selection(**soup_selection):
            # ['Countries of origin', 'New Zealand', 'United States']
            selection_list = css_selection.get_text("~").split("~")
            country = {"country": selection_list[1:]}

        return country

    @property
    def get_language(self) -> dict:
        language = {}

        soup_selection = {
            "soup": self.soup,
            "method": self.find,
            "tag": "li",
            "data-testid": "title-details-languages",
        }
        if css_selection := self.soup_selection(**soup_selection):
            # ['Languages', 'English', 'Sindarin']
            selection_list = css_selection.get_text("~").split("~")
            language = {"language": selection_list[1:]}

        return language

    @property
    def get_release_date(self) -> dict:
        release_date = {}

        soup_selection = {
            "soup": self.soup,
            "method": self.find,
            "tag": "li",
            "data-testid": "title-details-releasedate",
        }
        if css_selection := self.soup_selection(**soup_selection):
            # ['Release date', 'December 21, 2001 (Turkey)']
            selection_list = css_selection.get_text("~").split("~")
            regex_pattern = r"(^.*?\d{4})"
            search = regex_search(selection_list[1], regex_pattern)
            try:
                date_time = get_date_time(search, "%B %d. %Y")
            except ValueError:
                try:
                    date_time = get_date_time(search, "%B %d, %Y")
                except ValueError:
                    date_time = get_date_time(search, "%B %d. %Y")
            release_date = {"release_date": date_time}

        return release_date

    @property
    def get_title(self):
        title = {}

        soup_selection = {
            "soup": self.soup,
            "method": self.find,
            "tag": "h1",
            "data-testid": "hero-title-block__title",
        }
        if css_selection := self.soup_selection(**soup_selection):
            title = {"title": css_selection.text.strip()}

        return title

    @property
    def get_is_active(self) -> dict:
        is_active = {"is_active": False}

        soup_selection = {
            "soup": self.soup,
            "method": self.find,
            "tag": "a",
            "title": "See more release dates",
        }
        if css_selection := self.soup_selection(**soup_selection):
            text = css_selection.text.strip()
            if re.search(r"\d{4}–\s", text):
                is_active.update(is_active=True)

        return is_active

    @property
    def get_budget(self) -> dict:
        budget = {}

        soup_selection = {
            "soup": self.soup,
            "method": self.find,
            "tag": "li",
            "data-testid": "title-boxoffice-budget",
        }
        if css_selection := self.soup_selection(**soup_selection):
            # ['Budget', '$93,000,000 (estimated)']
            selection_list = css_selection.get_text("&").split("&")
            budget = {"budget": re.sub("[$,(estimad) ]", "", selection_list[-1])}

        return budget

    @property
    def get_usa_opening_weekend(self) -> dict:
        usa_opening_weekend = {}

        soup_selection = {
            "soup": self.soup,
            "method": self.find,
            "tag": "li",
            "data-testid": "title-boxoffice-openingweekenddomestic",
        }
        if css_selection := self.soup_selection(**soup_selection):
            # TODO: need currency control
            # ['Opening weekend US & Canada', '$47,211,490', 'Dec 23, 2001']
            selection_list = css_selection.get_text("~").split("~")
            usa_opening_weekend = {
                "usa_opening_weekend": re.sub("[$,]", "", selection_list[1])
            }

        return usa_opening_weekend

    @property
    def get_ww_gross(self) -> dict:
        ww_gross = {}

        soup_selection = {
            "soup": self.soup,
            "method": self.find,
            "tag": "li",
            "data-testid": "title-boxoffice-cumulativeworldwidegross",
        }
        if css_selection := self.soup_selection(**soup_selection):
            # ['Gross worldwide', '$897,690,072']
            selection_list = css_selection.get_text("~").split("~")
            ww_gross = {"ww_gross": re.sub("[$,]", "", selection_list[1])}

        return ww_gross

    @staticmethod
    def convert_runtime(runtime_str: str) -> int:
        """Convert string run time to integer value. Exp: 1h 32m to 92"""
        run_time_list = runtime_str.split("h")
        if len(run_time_list) > 1:
            hour = int(run_time_list[0]) * 60
            if minute := run_time_list[-1].strip("min"):
                minute = int(minute)
            run_time = hour + (minute or 0)
        elif run_time_list[0]:
            run_time = int(run_time_list[0].strip("min"))
        else:
            run_time = 0

        return run_time


class IMDBBase(
    IMDBEpisodes,
    IMDBCast,
    IMDBAwards,
    IMDBPersonalData,
    IMDBRating,
    IMDBHomePage,
    SoupSelectionMixin,
):  # NOQA: E501
    EPISODES = "episodes"
    FULL_CREDITS = "fullcredits"
    AWARDS = "awards"
    PERSONAL_DATA = "name"
    RATINGS = "ratings"
    BASE_URL = "https://www.imdb.com"

    def __init__(self, soup: BeautifulSoup, url: str, search_type: str):
        self.soup = soup
        self.url = url
        self.search_type = search_type

    def run(self) -> dict:
        result = {}
        if self.EPISODES in self.url:
            result.update(self.get_episodes)
        elif self.FULL_CREDITS in self.url:
            result.update(self.get_cast)
        elif self.AWARDS in self.url:
            result.update(self.get_awards)
        elif self.RATINGS in self.url:
            result.update(self.get_total_vote)
            result.update(self.get_average_rating)
        elif self.PERSONAL_DATA in self.url:
            result.update(self.get_birth_date)
            result.update(self.get_born_place)
            result.update(self.get_death_date)
            result.update(self.get_death_place)
            result.update(self.get_person_awards)
            result.update(self.get_perks)
        elif self.search_type == Movie.TYPE:
            result.update(self.get_genre)
            result.update(self.get_director)
            result.update(self.get_runtime)
            result.update(self.get_popularity)
            result.update(self.get_country)
            result.update(self.get_language)
            result.update(self.get_release_date)
            result.update(self.get_title)
            result.update(self.get_budget)
            result.update(self.get_usa_opening_weekend)
            result.update(self.get_ww_gross)
        elif self.search_type == Series.TYPE:
            result.update(self.get_genre)
            result.update(self.get_creator)
            result.update(self.get_director)
            result.update(self.get_runtime)
            result.update(self.get_popularity)
            result.update(self.get_country)
            result.update(self.get_language)
            result.update(self.get_release_date)
            result.update(self.get_title)
            result.update(self.get_is_active)

        return result
