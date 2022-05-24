from TvFY.movies.models import Movie
from TvFY.series.models import Series
from itests.base import BaseTestCase


class TomatoesMovieTestCase(BaseTestCase):
    def setUp(self) -> None:
        self.expected_attrs = {
            "rt_genre",
            "rt_director",
            "rt_director_url",
            "rt_tomatometer_rate",
            "rt_audience_rate",
            "storyline",
        }

    def test__lotr(self):
        url = "https://www.rottentomatoes.com/m/the_lord_of_the_rings_the_fellowship_of_the_ring"

        result = self.get_tomatoes_result(url=url, search_type=Movie.TYPE)

        self.assertTrue(self.is_subset(attrs=self.expected_attrs, results=result))

    def test__the_dark_knight(self):
        url = "https://www.rottentomatoes.com/m/the_dark_knight"

        result = self.get_tomatoes_result(url=url, search_type=Movie.TYPE)

        self.assertTrue(self.is_subset(attrs=self.expected_attrs, results=result))

    def test__spirited_away(self):
        url = "https://www.rottentomatoes.com/m/spirited_away"

        result = self.get_tomatoes_result(url=url, search_type=Movie.TYPE)

        self.assertTrue(self.is_subset(attrs=self.expected_attrs, results=result))


class TomatoesSeriesTestCase(BaseTestCase):
    def setUp(self) -> None:
        self.expected_attrs = {
            "rt_genre",
            "rt_tomatometer_rate",
            "rt_audience_rate",
            "network",
            "storyline",
        }

    def test__the_boys(self):
        url = "https://www.rottentomatoes.com/tv/the_boys_2019"

        result = self.get_tomatoes_result(url=url, search_type=Series.TYPE)

        self.assertTrue(self.is_subset(attrs=self.expected_attrs, results=result))

    def test__hunter_x_hunter(self):
        expected_attrs = self.expected_attrs.copy()
        expected_attrs.remove("rt_tomatometer_rate")
        url = "https://www.rottentomatoes.com/tv/hunter_x_hunter"

        result = self.get_tomatoes_result(url=url, search_type=Series.TYPE)

        self.assertTrue(self.is_subset(attrs=expected_attrs, results=result))

    def test__sherlock(self):
        url = "https://www.rottentomatoes.com/tv/sherlock"

        result = self.get_tomatoes_result(url=url, search_type=Series.TYPE)

        self.assertTrue(self.is_subset(attrs=self.expected_attrs, results=result))
