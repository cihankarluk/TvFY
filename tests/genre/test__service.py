from TvFY.genre.models import Genre
from TvFY.genre.service import GenreService
from tests.base import BaseTestCase


class GenreServiceTestCase(BaseTestCase):

    def test__load_genres(self):
        genre_query = Genre.objects.all()

        self.assertEqual(28, genre_query.count())

    def test__get_genre_ids(self):
        search_data = {"rt_genre": ["Action"], "test": ["Drama"]}

        result = GenreService.get_genre_ids(search_data=search_data)

        self.assertEqual(1, result.count())

    def test__get_genre_ids__empty_search_data(self):
        search_data = {}

        result = GenreService.get_genre_ids(search_data=search_data)

        self.assertFalse(result.exists())

