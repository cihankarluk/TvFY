import json
import logging
import re
import urllib.parse as urlparse
from collections import defaultdict
from datetime import datetime
from typing import Union, Optional, Any
from urllib.parse import parse_qs

from bs4 import BeautifulSoup

from TvFY.collector.helpers import SoupSelectionMixin
from TvFY.core.helpers import get_date_time, regex_search
from TvFY.movies.models import Movie
from TvFY.series.models import Series

logger = logging.getLogger(__name__)


class IMDBEpisodes:
    url: str
    find: str
    find_all: str
    soup_selection: classmethod
    soup: BeautifulSoup

    def get_imdb_vote_count(self, episode_data: BeautifulSoup) -> Optional[int]:
        vote_count = None

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
    def get_season(self) -> str:
        parsed = urlparse.urlparse(self.url)
        season = parse_qs(parsed.query)["season"][0]
        return season

    def get_episode_release_date(self, episode_data: BeautifulSoup) -> Optional[datetime]:
        episode_release_date = None

        soup_selection = {
            "soup": episode_data,
            "method": self.find,
            "tag": "div",
            "class": "airdate",
        }
        if css_selection := self.soup_selection(**soup_selection):
            episode_release_date = css_selection.text.strip()
            try:
                episode_release_date = get_date_time(episode_release_date, "%d %b. %Y")
            except ValueError:
                episode_release_date = get_date_time(episode_release_date, "%d %b %Y")

        return episode_release_date

    @property
    def get_episodes(self) -> dict[str, Any]:
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
                try:
                    imdb_rate = float(episode_data.find("span", class_="ipl-rating-star__rating").text)
                except AttributeError:
                    logger.error(f"Error while fetching imdb_rate! URL: {self.url}")
                    continue

                data = {
                    "title": episode_data.a["title"],
                    "storyline": episode_data.find("div", class_="item_description").text.strip(),
                    "imdb_rate": imdb_rate,
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
    BASE_URL: str

    @staticmethod
    def cast_information(cast_data: str) -> Union[bool, dict[str, Any]]:
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
    def get_cast(self) -> dict[str, list[dict[str, str]]]:
        cast_result = {}

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
                        try:
                            cast_information = {"character_name": character.a.text}
                        except AttributeError:
                            # Case for a.text is not accessible.
                            # In that case character does not have character name and no need to save.
                            continue
                    else:
                        cast_information = self.cast_information(character.get_text(" sp "))
                        if not cast_information:
                            continue

                    actor_detail = cast.find("td", class_="").a
                    actor = self.get_name(actor_detail.text.strip())
                    actor.update(cast_information)
                    actor.update({"imdb_actor_url": f'{self.BASE_URL}{actor_detail["href"].split("?")[0]}'})
                    results.append(actor)
            cast_result = {"cast": results}

        return cast_result


class IMDBAwards:
    url: str
    find: str
    soup_selection: classmethod
    soup: BeautifulSoup

    @property
    def get_actor_awards(self) -> dict[str, int]:
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
    def get_birth_date(self) -> dict[str, datetime]:
        born_date = {}

        soup_selection = {
            "soup": self.soup,
            "method": self.find,
            "tag": "div",
            "id": "name-born-info",
        }
        if css_selection := self.soup_selection(**soup_selection):
            if time := css_selection.time:
                try:
                    born_date = {"born_date": datetime.strptime(time["datetime"], "%Y-%m-%d")}
                except ValueError:
                    year = time["datetime"].split("-")[0]
                    born_date = {"born_date": datetime.strptime(year, "%Y")}

        return born_date

    @property
    def get_born_place(self) -> dict[str, str]:
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
    def get_death_date(self) -> dict[str, datetime]:
        died_date = {}

        soup_selection = {
            "soup": self.soup,
            "method": self.find,
            "tag": "div",
            "id": "name-death-info",
        }
        if css_selection := self.soup_selection(**soup_selection):
            died_date = {"died_date": datetime.strptime(css_selection.time["datetime"], "%Y-%m-%d")}

        return died_date

    @property
    def get_death_place(self) -> dict[str, str]:
        died_at = {}

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
    def get_person_awards(self) -> dict[str, int]:
        result = {}

        soup_selection = {
            "soup": self.soup,
            "method": self.find_all,
            "tag": "span",
            "class": "awards-blurb",
        }
        if css_selection := self.soup_selection(**soup_selection):
            oscar_data = css_selection[0].get_text(strip=True)
            search: Optional[int] = regex_search(oscar_data, r"\d{1,2}")
            if search and "Won" in oscar_data:
                result["oscars"] = search
            elif search and len(css_selection) > 1:
                # If there is no oscar wins and nominations
                result["oscar_nominations"] = search

            try:
                wins, nominations = re.findall(r"\d+", css_selection[-1].get_text(strip=True))
            except ValueError:
                # Case for there is nomination however no wins.
                wins = 0
                nominations = re.findall(r"\d+", css_selection[-1].get_text(strip=True))[0]

            result["wins"] = wins
            result["nominations"] = nominations

        return result

    @property
    def get_perks(self) -> dict[str, list[str]]:
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


class IMDBHomePage:
    url: str
    find: str
    find_all: str
    soup_selection: classmethod
    soup: BeautifulSoup
    get_name: classmethod
    BASE_URL: str

    @property
    def get_genre(self) -> dict[str, list[str]]:
        genres = {}

        soup_selection = {
            "soup": self.soup,
            "method": self.find,
            "tag": "script",
            "id": "__NEXT_DATA__",
        }
        if css_selection := self.soup_selection(**soup_selection):
            data = json.loads(css_selection.next_element)["props"]["pageProps"]
            genre_list = [
                item["text"] for item in data["aboveTheFoldData"]["genres"]["genres"]
            ]
            genres = {"imdb_genre": genre_list}

        return genres

    @property
    def get_creator(self) -> dict[str, str]:
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
                "imdb_creator_url": f'{self.BASE_URL}{css_selection.a["href"].split("?")[0]}',
            }

        return creator

    @property
    def get_director(self) -> dict[str, str]:
        director = {}

        soup_selection = {
            "soup": self.soup,
            "method": self.find,
            "tag": "a",
            "class": "ipc-metadata-list-item__list-content-item ipc-metadata-list-item__list-content-item--link",
        }
        if css_selection := self.soup_selection(**soup_selection):
            director = {
                "imdb_director": self.get_name(css_selection.get_text(strip=True)),
                "imdb_director_url": f'{self.BASE_URL}{css_selection["href"].split("?")[0]}',
            }

        return director

    @property
    def get_runtime(self) -> dict[str, int]:
        runtime = {}

        soup_selection = {
            "soup": self.soup,
            "method": self.find,
            "tag": "script",
            "id": "__NEXT_DATA__",
        }
        if css_selection := self.soup_selection(**soup_selection):
            data = json.loads(css_selection.next_element)
            runtime = {"run_time": data["props"]["pageProps"]["mainColumnData"]["runtime"]["seconds"]}

        return runtime

    @property
    def get_popularity(self) -> dict[str, int]:
        imdb_popularity = {}

        soup_selection = {
            "soup": self.soup,
            "method": self.find,
            "tag": "div",
            "data-testid": "hero-rating-bar__popularity__score",
        }
        if css_selection := self.soup_selection(**soup_selection):
            imdb_popularity = {"imdb_popularity": int(css_selection.text.replace(",", ""))}

        return imdb_popularity

    @property
    def get_country(self) -> dict[str, list[str]]:
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
    def get_language(self) -> dict[str, list[str]]:
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
    def get_release_date(self) -> dict[str, datetime]:
        release_date = {}

        soup_selection = {
            "soup": self.soup,
            "method": self.find,
            "tag": "script",
            "id": "__NEXT_DATA__",
        }
        if css_selection := self.soup_selection(**soup_selection):
            data = json.loads(css_selection.next_element)
            rd_data = data["props"]["pageProps"]["aboveTheFoldData"]["releaseDate"]
            date = f"{rd_data['day']} {rd_data['month']} {rd_data['year']}"
            release_date = {"release_date": get_date_time(date=date, pattern="%d %m %Y")}

        return release_date

    @property
    def get_title(self) -> dict[str, str]:
        title = {}

        soup_selection = {
            "soup": self.soup,
            "method": self.find,
            "tag": "h1",
            "data-testid": "hero-title-block__title",
        }
        if css_selection := self.soup_selection(**soup_selection):
            title = {"imdb_title": css_selection.text.strip()}

        return title

    @property
    def get_is_active(self) -> dict[str, Union[datetime, bool]]:
        is_active = {"is_active": True}

        soup_selection = {
            "soup": self.soup,
            "method": self.find,
            "tag": "script",
            "id": "__NEXT_DATA__",
        }
        if css_selection := self.soup_selection(**soup_selection):
            data = json.loads(css_selection.next_element)["props"]["pageProps"]
            if end_year := data["aboveTheFoldData"]["releaseYear"].get("endYear"):
                is_active["end_date"] = get_date_time(date=str(end_year), pattern="%Y")
                is_active["is_active"] = False

        return is_active

    @property
    def get_budget(self) -> dict[str, int]:
        budget = {}

        soup_selection = {
            "soup": self.soup,
            "method": self.find,
            "tag": "script",
            "id": "__NEXT_DATA__",
        }
        if css_selection := self.soup_selection(**soup_selection):
            data = json.loads(css_selection.next_element)["props"]["pageProps"]
            if production_budget := data["mainColumnData"]["productionBudget"]:
                budget.update({
                    "budget_amount": production_budget["budget"]["amount"],
                    "budget_currency": production_budget["budget"]["currency"]
                })

        return budget

    @property
    def get_usa_opening_weekend(self) -> dict[str, int]:
        usa_opening_weekend = {}

        soup_selection = {
            "soup": self.soup,
            "method": self.find,
            "tag": "script",
            "id": "__NEXT_DATA__",
        }
        if css_selection := self.soup_selection(**soup_selection):
            data = json.loads(css_selection.next_element)
            if uaw_data := data["props"]["pageProps"]["mainColumnData"].get("openingWeekendGross"):
                usa_opening_weekend.update({
                    "usa_ow_amount": uaw_data["gross"]["total"]["amount"],
                    "usa_ow_currency": uaw_data["gross"]["total"]["currency"],
                })

        return usa_opening_weekend

    @property
    def get_ww_gross(self) -> dict[str, int]:
        ww_gross = {}

        soup_selection = {
            "soup": self.soup,
            "method": self.find,
            "tag": "script",
            "id": "__NEXT_DATA__",
        }
        if css_selection := self.soup_selection(**soup_selection):
            data = json.loads(css_selection.next_element)["props"]["pageProps"]
            if ww_data := data["mainColumnData"]["worldwideGross"]:
                ww_gross.update({
                    "ww_amount": ww_data["total"]["amount"],
                    "ww_currency": ww_data["total"]["currency"],
                })
        return ww_gross

    @property
    def get_metacritic_score(self) -> dict[str, int]:
        metacritic_score = {}

        soup_selection = {
            "soup": self.soup,
            "method": self.find,
            "tag": "script",
            "id": "__NEXT_DATA__",
        }
        if css_selection := self.soup_selection(**soup_selection):
            data = json.loads(css_selection.next_element)
            if mc_score := data["props"]["pageProps"]["aboveTheFoldData"]["metacritic"]:
                metacritic_score = {"metacritic_score": mc_score["metascore"]["score"]}

        return metacritic_score

    @property
    def get_ratings_score(self) -> dict[str, int]:
        imdb_rating = {}

        soup_selection = {
            "soup": self.soup,
            "method": self.find,
            "tag": "script",
            "id": "__NEXT_DATA__",
        }
        if css_selection := self.soup_selection(**soup_selection):
            data = json.loads(css_selection.next_element)
            if rating := data["props"]["pageProps"]["aboveTheFoldData"]["ratingsSummary"]:
                imdb_rating = {
                    "imdb_vote_count": rating["voteCount"],
                    "imdb_rate": rating["aggregateRating"],
                }

        return imdb_rating

    @property
    def get_awards(self) -> dict[str, int]:
        awards = {}

        soup_selection = {
            "soup": self.soup,
            "method": self.find,
            "tag": "script",
            "id": "__NEXT_DATA__",
        }
        if css_selection := self.soup_selection(**soup_selection):
            data = json.loads(css_selection.next_element)["props"]["pageProps"]
            awards = {
                "wins": data["mainColumnData"]["wins"]["total"],
                "nominations": data["mainColumnData"]["nominations"]["total"],
                "oscar_wins": 0,
                "oscar_nominations": 0
            }
            if prestigious_awards := data["mainColumnData"]["prestigiousAwardSummary"]:
                awards.update({
                    "oscar_wins": prestigious_awards.get("wins", 0),
                    "oscar_nominations": prestigious_awards.get("nominations", 0),
                })

        return awards

    @property
    def get_season_episode_count(self) -> dict[str, int]:
        season_episode_count = {}

        soup_selection = {
            "soup": self.soup,
            "method": self.find,
            "tag": "script",
            "id": "__NEXT_DATA__",
        }
        if css_selection := self.soup_selection(**soup_selection):
            data = json.loads(css_selection.next_element)["props"]["pageProps"]
            if episode_data := data["mainColumnData"]["episodes"]:
                season_episode_count = {
                    "episode_count": episode_data["episodes"]["total"],
                    "season_count": len(episode_data["seasons"]),
                }
        return season_episode_count


class IMDBBase(
    IMDBEpisodes,
    IMDBCast,
    IMDBAwards,
    IMDBPersonalData,
    IMDBHomePage,
    SoupSelectionMixin,
):
    EPISODES = "episodes"
    CAST = "fullcredits"
    AWARDS = "awards"
    PERSONAL_DATA = "name"
    BASE_URL = "https://www.imdb.com"

    def __init__(self, soup: BeautifulSoup, url: str, search_type: str):
        self.soup = soup
        self.url = url
        self.search_type = search_type

    def run(self) -> dict[str, Any]:
        logger.warning(f"IMDB web scrapping started for {self.url}")
        result = {self.url: {}}
        if self.EPISODES in self.url:
            result[self.url].update(self.get_episodes)
        elif self.CAST in self.url:
            result[self.url].update(self.get_cast)
        elif self.AWARDS in self.url:
            result.update(self.get_actor_awards)
        elif self.PERSONAL_DATA in self.url:
            result[self.url].update(self.get_birth_date)
            result[self.url].update(self.get_born_place)
            result[self.url].update(self.get_death_date)
            result[self.url].update(self.get_death_place)
            result[self.url].update(self.get_person_awards)
            result[self.url].update(self.get_perks)
        elif self.search_type == Movie.TYPE:
            result[self.url].update(self.get_genre)
            result[self.url].update(self.get_director)
            result[self.url].update(self.get_runtime)
            result[self.url].update(self.get_popularity)
            result[self.url].update(self.get_country)
            result[self.url].update(self.get_language)
            result[self.url].update(self.get_release_date)
            result[self.url].update(self.get_title)
            result[self.url].update(self.get_budget)
            result[self.url].update(self.get_usa_opening_weekend)
            result[self.url].update(self.get_ww_gross)
            result[self.url].update(self.get_metacritic_score)
            result[self.url].update(self.get_ratings_score)
            result[self.url].update(self.get_awards)
        elif self.search_type == Series.TYPE:
            result[self.url].update(self.get_genre)
            result[self.url].update(self.get_creator)
            result[self.url].update(self.get_director)
            result[self.url].update(self.get_runtime)
            result[self.url].update(self.get_popularity)
            result[self.url].update(self.get_country)
            result[self.url].update(self.get_language)
            result[self.url].update(self.get_release_date)
            result[self.url].update(self.get_title)
            result[self.url].update(self.get_is_active)
            result[self.url].update(self.get_metacritic_score)
            result[self.url].update(self.get_ratings_score)
            result[self.url].update(self.get_season_episode_count)
            result[self.url].update(self.get_awards)

        return result
