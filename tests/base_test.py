from django.test import TestCase

from TvFY.movies.models import Movie
from TvFY.series.models import Series


class BaseTest(TestCase):
    def setUp(self) -> None:
        self.series = Series.type
        self.movie = Movie.type

    def control_home_page(self, result):
        self.assertTrue(result["country"])
        self.assertTrue(result["creator"])
        self.assertTrue(result["language"])
        self.assertTrue(result["popularity"])
        self.assertTrue(result["genres_imdb"])
        self.assertTrue(result["wins"])
        self.assertTrue(result["nominations"])
