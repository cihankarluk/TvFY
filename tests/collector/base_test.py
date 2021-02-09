from django.test import TestCase

from TvFY.movies.models import Movie
from TvFY.series.models import Series


class BaseTest(TestCase):
    def setUp(self) -> None:
        self.series = Series.TYPE
        self.movie = Movie.TYPE

    def imdb_control_home_page(self, result):
        self.assertTrue(result["country"])
        self.assertTrue(result["creator"])
        self.assertTrue(result["language"])
        self.assertTrue(result["popularity"])
        self.assertTrue(result["imdb_genre"])
        self.assertTrue(result["nominations"])
        self.assertTrue(result["release_date"])
        self.assertTrue(result["title"])
        self.assertTrue(result["total_imdb_rate"])
        self.assertTrue(result["total_imdb_vote_count"])
        self.assertTrue(result["imdb_creator_url"])

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
        self.assertTrue(result["rt_creator_url"])
