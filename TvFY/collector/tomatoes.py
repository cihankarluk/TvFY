import json

from bs4 import BeautifulSoup

from TvFY.collector.helpers import SoupSelectionMixin
from TvFY.movies.models import Movie
from TvFY.series.models import Series


class RottenTomatoesMovieHomePage:
    find: str
    soup_selection: classmethod
    soup: BeautifulSoup
    get_name: classmethod
    BASE_URL: str

    @property
    def get_movie_genre(self) -> dict[str, list[str]]:
        genres = {}

        soup_selection = {
            "soup": self.soup,
            "method": self.find,
            "tag": "div",
            "class": "meta-value genre",
            "data-qa": "movie-info-item-value",
        }
        if css_selection := self.soup_selection(**soup_selection):
            genres = {"rt_genre": [genre.strip() for genre in css_selection.text.split(",")]}

        return genres

    @property
    def get_movie_director(self) -> dict[str, str]:
        director = {}

        soup_selection = {
            "soup": self.soup,
            "method": self.find,
            "tag": "a",
            "data-qa": "movie-info-director",
        }
        if css_selection := self.soup_selection(**soup_selection):
            director = {
                "rt_director": self.get_name(css_selection.get_text(strip=True)),
                "rt_director_url": f"{self.BASE_URL}{css_selection['href']}",
            }

        return director

    @property
    def get_movie_ratings(self) -> dict[str, int]:
        ratings = {}

        soup_selection = {
            "soup": self.soup,
            "method": self.find,
            "tag": "script",
            "id": "score-details-json",
        }
        if css_selection := self.soup_selection(**soup_selection):
            data = json.loads(css_selection.next_element)["scoreboard"]
            ratings = {
                "rt_audience_rate": data["audienceScore"],
                "rt_audience_count": data["audienceCount"],
                "rt_tomatometer_rate": data["tomatometerScore"],
                "rt_tomatometer_count": data["tomatometerCount"],
            }

        return ratings

    @property
    def get_movie_title(self) -> dict[str, str]:
        rt_title = {}

        soup_selection = {
            "soup": self.soup,
            "method": self.find,
            "tag": "h1",
            "class": "scoreboard__title",
        }
        if css_selection := self.soup_selection(**soup_selection):
            rt_title = {"rt_title": css_selection.text}

        return rt_title


class RottenTomatoesSeriesHomePage:
    find: str
    soup_selection: classmethod
    soup: BeautifulSoup

    @property
    def get_series_average_tomatometer(self) -> dict:
        average_tomatometer = {}

        soup_selection = {
            "soup": self.soup,
            "method": self.find,
            "tag": "span",
            "class": "mop-ratings-wrap__percentage",
            "data-qa": "tomatometer",
        }
        if css_selection := self.soup_selection(**soup_selection):
            average_tomatometer = {"rt_tomatometer_rate": int(css_selection.get_text(strip=True).replace("%", ""))}

        return average_tomatometer

    @property
    def get_series_audience_rate(self) -> dict[str, int]:
        audience_rate = {}

        soup_selection = {
            "soup": self.soup,
            "method": self.find,
            "tag": "span",
            "class": "mop-ratings-wrap__percentage",
            "data-qa": "audience-score",
        }
        if css_selection := self.soup_selection(**soup_selection):
            audience_rate = {"rt_audience_rate": int(css_selection.get_text(strip=True).replace("%", ""))}

        return audience_rate

    @property
    def get_series_genre(self) -> dict[str, list[str]]:
        genre = {}

        soup_selection = {
            "soup": self.soup,
            "method": self.find,
            "tag": "td",
            "data-qa": "series-details-genre",
        }
        if css_selection := self.soup_selection(**soup_selection):
            genre = {"rt_genre": [css_selection.get_text(strip=True)]}

        return genre

    @property
    def get_series_tv_network(self) -> dict[str, list[str]]:
        tv_network = {}

        soup_selection = {
            "soup": self.soup,
            "method": self.find,
            "tag": "td",
            "data-qa": "series-details-network",
        }
        if css_selection := self.soup_selection(**soup_selection):
            tv_network = {"tv_network": css_selection.get_text(strip=True)}

        return tv_network

    @property
    def get_storyline(self) -> dict[str, str]:
        storyline = {}

        soup_selection = {
            "soup": self.soup,
            "method": self.find,
            "tag": "div",
            "id": "movieSynopsis",
        }
        if css_selection := self.soup_selection(**soup_selection):
            storyline = {"rt_storyline": css_selection.get_text(strip=True)}

        return storyline


class RottenTomatoesBase(
    RottenTomatoesMovieHomePage,
    RottenTomatoesSeriesHomePage,
    SoupSelectionMixin
):
    BASE_URL = "https://www.rottentomatoes.com"

    def __init__(self, soup: BeautifulSoup, url: str, search_type: str):
        self.soup = soup
        self.url = url
        self.search_type = search_type

    def run(self) -> dict[str, ...]:
        result = {}
        result[self.url] = {}
        if self.search_type == Movie.TYPE:
            result[self.url].update(self.get_movie_genre)
            result[self.url].update(self.get_movie_director)
            result[self.url].update(self.get_movie_ratings)
            result[self.url].update(self.get_storyline)
            result[self.url].update(self.get_movie_title)
        elif self.search_type == Series.TYPE:
            result[self.url].update(self.get_series_genre)
            result[self.url].update(self.get_series_average_tomatometer)
            result[self.url].update(self.get_series_audience_rate)
            result[self.url].update(self.get_series_tv_network)
            result[self.url].update(self.get_storyline)
        return result
