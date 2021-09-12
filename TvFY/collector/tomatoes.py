from bs4 import BeautifulSoup

from TvFY.collector.helpers import SoupSelectionMixin
from TvFY.movies.models import Movie
from TvFY.series.models import Series


class TomatoesMovieHomePage:
    find: str
    soup_selection: classmethod
    soup: BeautifulSoup
    get_name: classmethod
    BASE_URL: str

    @property
    def get_movie_genre(self) -> dict:
        genres = {}

        soup_selection = {
            "soup": self.soup,
            "method": self.find,
            "tag": "div",
            "class": "meta-value genre",
            "dataset-qa": "movie-info-item-value",
        }
        if css_selection := self.soup_selection(**soup_selection):
            genres = {
                "rt_genre": [genre.strip() for genre in css_selection.text.split(",")]
            }

        return genres

    @property
    def get_movie_director(self) -> dict:
        director = {}

        soup_selection = {
            "soup": self.soup,
            "method": self.find,
            "tag": "a",
            "dataset-qa": "movie-info-director",
        }
        if css_selection := self.soup_selection(**soup_selection):
            director = {
                "rt_director": self.get_name(css_selection.get_text(strip=True)),
                "rt_director_url": f"{self.BASE_URL}{css_selection['href']}",
            }

        return director

    @property
    def get_movie_ratings(self) -> dict:
        ratings = {}

        soup_selection = {
            "soup": self.soup,
            "method": self.find,
            "class": "scoreboard",
            "dataset-qa": "score-panel",
        }
        if css_selection := self.soup_selection(**soup_selection):
            ratings = {
                "rt_audience_rate": int(css_selection["audiencescore"]),
                "rt_tomatometer_rate": int(css_selection["tomatometerscore"]),
            }

        return ratings


class TomatoesSeriesHomePage:
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
            "dataset-qa": "tomatometer",
        }
        if css_selection := self.soup_selection(**soup_selection):
            average_tomatometer = {
                "rt_tomatometer_rate": css_selection.get_text(strip=True).replace("%", "")
            }

        return average_tomatometer

    @property
    def get_series_audience_rate(self) -> dict:
        audience_rate = {"audience_rate": None}

        soup_selection = {
            "soup": self.soup,
            "method": self.find,
            "tag": "span",
            "class": "mop-ratings-wrap__percentage",
            "dataset-qa": "audience-score",
        }
        if css_selection := self.soup_selection(**soup_selection):
            audience_rate = {
                "rt_audience_rate": int(
                    css_selection.get_text(strip=True).replace("%", "")
                )
            }

        return audience_rate

    @property
    def get_series_genre(self) -> dict:
        genre = {}

        soup_selection = {
            "soup": self.soup,
            "method": self.find,
            "tag": "td",
            "dataset-qa": "series-details-genre",
        }
        if css_selection := self.soup_selection(**soup_selection):
            genre = {"rt_genre": [css_selection.get_text(strip=True)]}

        return genre

    @property
    def get_series_network(self) -> dict:
        network = {}

        soup_selection = {
            "soup": self.soup,
            "method": self.find,
            "tag": "td",
            "dataset-qa": "series-details-network",
        }
        if css_selection := self.soup_selection(**soup_selection):
            network = {"network": css_selection.get_text(strip=True)}

        return network

    @property
    def get_storyline(self) -> dict:
        storyline = {}

        soup_selection = {
            "soup": self.soup,
            "method": self.find,
            "tag": "div",
            "id": "movieSynopsis",
        }
        if css_selection := self.soup_selection(**soup_selection):
            storyline = {"storyline": css_selection.get_text(strip=True)}

        return storyline


class TomatoesBase(TomatoesMovieHomePage, TomatoesSeriesHomePage, SoupSelectionMixin):
    BASE_URL = "https://www.rottentomatoes.com"

    def __init__(self, soup, url, search_type):
        self.soup = soup
        self.url = url
        self.search_type = search_type

    def run(self):
        """
        Keys: 'rt_genre', 'rt_tomatometer_rate', 'rt_audience_rate', 'network', 'storyline'
        """
        result = {}
        if self.search_type == Movie.TYPE:
            result.update(self.get_movie_genre)
            result.update(self.get_movie_director)
            result.update(self.get_movie_ratings)
            result.update(self.get_storyline)
        elif self.search_type == Series.TYPE:
            result.update(self.get_series_genre)
            result.update(self.get_series_average_tomatometer)
            result.update(self.get_series_audience_rate)
            result.update(self.get_series_network)
            result.update(self.get_storyline)
        return result
