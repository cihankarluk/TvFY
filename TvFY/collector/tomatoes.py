import bs4

from TvFY.collector.helpers import SoupSelectionMixin
from TvFY.series.models import Series


class TomatoesMovie(SoupSelectionMixin):
    run_method: classmethod
    director = 'Director:'

    @property
    def get_tomatometer_movie(self) -> dict:
        rating = {}
        css_selection = self.soup_selection(
            self.find, selection="mop-ratings-wrap__half", tag="div"
        )
        selection = css_selection.find("span", class_="mop-ratings-wrap__percentage")
        if selection:
            rating.update(
                {"rt_tomatometer": int(selection.text.strip().replace("%", ""))}
            )

        count_selection = css_selection.find("small")
        if count_selection:
            rating.update(
                {"rt_tomatometer_count": int(count_selection.text.strip())}
            )
        return rating

    @property
    def get_audience_rate_movie(self) -> dict:
        rating = {}
        css_selection = self.soup_selection(
            self.find, selection="mop-ratings-wrap__half audience-score", tag="div"
        )
        selection = css_selection.find("span", class_="mop-ratings-wrap__percentage")
        if selection:
            rating.update(
                {"rt_audience_rate": int(selection.text.strip().replace("%", ""))}
            )

        count_selection = css_selection.find("strong")
        if count_selection:
            # User Ratings: 1,057,449
            count = count_selection.text.strip().split(": ")[1].replace(",", "")
            rating.update(
                {"rt_audience_rate_count": int(count)}
            )
        return rating

    def get_director(self, content: bs4) -> dict:
        director = {}
        selection = content.find("div", class_="meta-label subtle")
        if selection and selection.text == self.director:
            director_name = content.find("div", class_="meta-value").text.strip()
            director = {
                "director": self.get_name(director_name)
            }
        return director

    @staticmethod
    def get_rt_genre_movie(content: bs4) -> dict:
        genres = {}
        selection = content.find("div", class_="meta-value genre")
        if selection:
            genres = {"rt_genre": [genre.strip() for genre in selection.text.split(",")]}
        return genres

    @property
    def split_details_movie(self) -> dict:
        result = {}
        actions = ["get_director", "get_rt_genre_movie"]
        css_sub_selection = self.soup_selection(
            self.find, selection="panel-body content_body", tag="div"
        )
        for div in css_sub_selection.find_all("li"):
            for index, action in enumerate(actions):
                if data := self.run_method(action, div):
                    actions.pop(index)
                    result.update(data)
            if not actions:
                break
        return result


class TomatoesSeries(SoupSelectionMixin):
    run_method: classmethod
    genre = 'Genre:'
    network = 'TV Network:'

    @property
    def get_tomatometer(self) -> dict:
        rating = {}
        css_selection = self.soup_selection(
            self.find, selection="mop-ratings-wrap__half critic-score", tag="div"
        )
        selection = css_selection.find("span", class_="mop-ratings-wrap__percentage")
        if selection:
            # 90%
            rating = {"rt_tomatometer": int(selection.text.strip().replace("%", ""))}
        return rating

    @property
    def get_audience_rate(self) -> dict:
        rating = {}
        css_selection = self.soup_selection(
            self.find, selection="mop-ratings-wrap__half audience-score", tag="div"
        )
        selection = css_selection.find("span", class_="mop-ratings-wrap__percentage")
        if selection:
            # 90%
            rating = {"rt_audience_rate": int(selection.text.strip().replace("%", ""))}
        return rating

    def get_rt_genre(self, content: bs4) -> dict:
        genres = {}
        if content.td and content.td.text == self.genre:
            css_selection = content.find_all("td")[-1]
            genres = {"rt_genre": css_selection.text.split(" & ")}
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
        css_sub_selection = self.soup_selection(
            self.find, tag="table"
        )
        for div in css_sub_selection.find_all("tr"):
            for index, action in enumerate(actions):
                if data := self.run_method(action, div):
                    actions.pop(index)
                    result.update(data)
            if not actions:
                break
        return result


class TomatoesScrapper(TomatoesMovie, TomatoesSeries):
    def __init__(self, soup, url, search_type):
        self.soup = soup
        self.url = url
        self.search_type = search_type

    def run_method(self, action: str, content: str):
        action_class: dict = {
            "get_rt_genre": self.get_rt_genre,
            "get_network": self.get_network,
            "get_rt_genre_movie": self.get_rt_genre_movie,
            "get_director": self.get_director
        }
        action_method: classmethod = action_class[action]
        return action_method(content=content)

    @property
    def get_storyline(self) -> dict:
        css_selection = self.soup_selection(
            self.select_one, selection="#movieSynopsis"
        )
        result = {"storyline": css_selection.text.strip()}
        return result

    def run(self):
        result = self.get_storyline
        if self.search_type == Series.type:
            result.update(self.split_details)
            result.update(self.get_tomatometer)
            result.update(self.get_audience_rate)
        else:
            result.update(self.split_details_movie)
            result.update(self.get_tomatometer_movie)
            result.update(self.get_audience_rate_movie)
        return result
