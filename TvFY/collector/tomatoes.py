import bs4

from TvFY.collector.helpers import SoupSelectionMixin
from TvFY.core.helpers import regex_search
from TvFY.series.models import Series


class TomatoesMovie(SoupSelectionMixin):
    run_method: classmethod

    @property
    def get_tomatometer_movie(self) -> dict:
        css_selection = self.soup_selection(
            soup=self.soup,
            method=self.find,
            tag="score-board",
        )
        if not css_selection:
            return {}

        str_soup = str(css_selection)
        score_int = int(css_selection["tomatometerscore"])
        regex_pattern = r'critics-count">\d{1,3}'
        rate_count = regex_search(content=str_soup, pattern=regex_pattern)
        rate_count_int = int(rate_count.strip('critics-count">').replace(",", ""))

        rating = {"rt_tomatometer": score_int, "rt_tomatometer_count": rate_count_int}
        return rating

    @property
    def get_audience_rate_movie(self) -> dict:
        css_selection = self.soup_selection(
            soup=self.soup,
            method=self.find,
            tag="score-board",
        )
        if not css_selection:
            return {}

        str_soup = str(css_selection)
        score_int = int(css_selection["audiencescore"])
        regex_pattern = r'audience-count">\d{1,3},\d{1,3}'
        rate_count = regex_search(content=str_soup, pattern=regex_pattern)
        rate_count_int = int(rate_count.strip('audience-count">').replace(",", ""))

        rating = {
            "rt_audience_rate": score_int,
            "rt_audience_rate_count": rate_count_int,
        }
        return rating

    @property
    def get_director(self) -> dict:
        css_selection = self.soup_selection(
            soup=self.soup,
            method=self.find,
            tag="a",
            **{"data-qa": "movie-info-director"},
        )
        if not css_selection:
            return {}

        director = {
            "director": self.get_name(css_selection.text),
            "rt_creator_url": css_selection["href"],
        }
        return director

    @property
    def get_rt_genre_movie(self) -> dict:
        css_selection = self.soup_selection(
            soup=self.soup, method=self.find, tag="div", class_="meta-value genre"
        )
        if not css_selection:
            return {}

        genres = {
            "rt_genre": [
                genre.strip().capitalize() for genre in css_selection.text.split(",")
            ]
        }
        return genres


class TomatoesSeries(SoupSelectionMixin):
    run_method: classmethod
    genre = "Genre:"
    network = "TV Network:"

    @property
    def get_tomatometer(self) -> dict:
        rating = {}
        css_selection = self.soup_selection(
            soup=self.soup,
            method=self.find,
            tag="div",
            class_="mop-ratings-wrap__half critic-score",
        )
        if not css_selection:
            return {}

        selection = css_selection.find("span", class_="mop-ratings-wrap__percentage")
        if selection:
            # 90%
            rating = {"rt_tomatometer": int(selection.text.strip().replace("%", ""))}
        return rating

    @property
    def get_audience_rate(self) -> dict:
        rating = {}
        css_selection = self.soup_selection(
            soup=self.soup,
            method=self.find,
            tag="div",
            class_="mop-ratings-wrap__half audience-score",
        )
        if not css_selection:
            return {}

        if rate := css_selection.find("span", class_="mop-ratings-wrap__percentage"):
            # 90%
            rating = {"rt_audience_rate": int(rate.text.strip().replace("%", ""))}
        return rating

    def get_rt_genre(self, content: bs4) -> dict:
        genres = {}
        if content.td and content.td.text == self.genre:
            css_selection = content.find_all("td")[-1]
            genres = [genre.capitalize() for genre in css_selection.text.split(" & ")]
            genres = {"rt_genre": genres}
        return genres

    def get_network(self, content: bs4) -> dict:
        network = {}
        if content.td and content.td.text == self.network:
            css_selection = content.find_all("td")[-1]
            network = {"network": css_selection.text}
        return network

    @property
    def split_details(self) -> dict:
        result = {}
        actions = ["get_rt_genre", "get_network"]
        css_selection = self.soup_selection(
            soup=self.soup, method=self.find, tag="section", id="detail_panel"
        )
        if not css_selection:
            return {}

        for div in css_selection.find_all("tr"):
            for index, action in enumerate(actions):
                if data := self.run_method(action, div):
                    actions.pop(index)
                    result.update(data)
            if not actions:
                break
        return result


class TomatoesScrapper(TomatoesMovie, TomatoesSeries):
    BASE_URL = "https://www.rottentomatoes.com"

    def __init__(self, soup, url, search_type):
        self.soup = soup
        self.url = url
        self.search_type = search_type

    def run_method(self, action: str, content: str):
        action_class: dict = {
            "get_rt_genre": self.get_rt_genre,
            "get_network": self.get_network,
            "get_rt_genre_movie": self.get_rt_genre_movie,
        }
        action_method: classmethod = action_class[action]
        return action_method(content=content)

    @property
    def get_storyline(self) -> dict:
        css_selection = self.soup_selection(
            soup=self.soup, method=self.select_one, selector="#movieSynopsis"
        )
        if not css_selection:
            return {}

        result = {"storyline": css_selection.text.strip()}
        return result

    def run(self):
        result = self.get_storyline
        if self.search_type == Series.TYPE:
            result.update(self.split_details)
            result.update(self.get_tomatometer)
            result.update(self.get_audience_rate)
        else:
            result.update(self.get_director)
            result.update(self.get_rt_genre_movie)
            result.update(self.get_tomatometer_movie)
            result.update(self.get_audience_rate_movie)
        return result
