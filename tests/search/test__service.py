from TvFY.movies.models import Movie
from TvFY.search.service import SearchService
from TvFY.series.models import Series
from tests.base import BaseTestCase


class SearchServiceTestCase(BaseTestCase):

    def test__get_urls(self):
        expected_list = [
            'https://www.imdb.com/title/tt1190634/fullcredits',
            'https://www.imdb.com/title/tt1190634/awards',
            'https://www.imdb.com/title/tt1190634/episodes?season=1',
            'https://www.imdb.com/title/tt1190634/'
        ]

        google_data = {"imdb_url": "https://www.imdb.com/title/tt1190634/"}

        urls = SearchService.get_urls(google_data=google_data, search_type=Series.TYPE)

        self.assertListEqual(expected_list, urls)

    def test__get_urls_movie(self):
        expected_list = [
            'https://www.imdb.com/title/tt1190634/fullcredits',
            'https://www.imdb.com/title/tt1190634/awards',
            'https://www.imdb.com/title/tt1190634/'
        ]

        google_data = {"imdb_url": "https://www.imdb.com/title/tt1190634/"}

        urls = SearchService.get_urls(google_data=google_data, search_type=Movie.TYPE)

        self.assertListEqual(expected_list, urls)