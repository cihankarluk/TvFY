from TvFY.genre.models import Genre
from TvFY.genre.service import GenreService
from tests.base import BaseTestCase


class GenreServiceTestCase(BaseTestCase):
    def test__insert_genre_fixtures(self):
        GenreService.insert_genre_fixtures()

        genre_query = Genre.objects.all()

        self.assertEqual(28, genre_query.count())
