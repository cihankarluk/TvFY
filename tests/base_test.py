from django.test import TestCase

from TvFY.movies.models import Movie
from TvFY.series.models import Series


class BaseTest(TestCase):
    def setUp(self) -> None:
        self.series = Series.type
        self.movie = Movie.type

    def imdb_control_home_page(self, result):
        self.assertTrue(result["country"])
        self.assertTrue(result["creator"])
        self.assertTrue(result["language"])
        self.assertTrue(result["popularity"])
        self.assertTrue(result["genres_imdb"])
        self.assertTrue(result["wins"])
        self.assertTrue(result["nominations"])
        self.assertTrue(result["release_date"])

    def rt_control_home_page(self, result):
        self.assertTrue(result["network"])
        self.assertTrue(result["rt_genre"])
        self.assertTrue(result["rt_tomatometer"])
        self.assertTrue(result["rt_audience_rate"])
        self.assertTrue(result["storyline"])

    def rt_control_home_page_movie(self, result):
        self.assertTrue(result["storyline"])
        self.assertTrue(result["director"])
        self.assertTrue(result["rt_genre"])
        self.assertTrue(result["rt_tomatometer"])
        self.assertTrue(result["rt_tomatometer_count"])
        self.assertTrue(result["rt_audience_rate"])
        self.assertTrue(result["rt_audience_rate_count"])
