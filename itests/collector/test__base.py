from TvFY.movies.models import Movie
from TvFY.series.models import Series
from itests.base import BaseTestCase


class ScrapperTestCase(BaseTestCase):
    def test__broken_url(self):
        urls = [
            "https://www.imdb.com/title/broken_url_test/",
        ]

        with self.assertRaises(AssertionError):
            self.get_scrapper_result(urls=urls, search_type=Series.TYPE)

    def test__the_boys(self):
        series_expected_attrs = {
            'https://www.rottentomatoes.com/tv/the_boys_2019/',
            'https://www.imdb.com/title/tt1190634/awards/',
            'https://www.imdb.com/title/tt1190634/',
            'https://www.imdb.com/title/tt1190634/ratings/',
            'https://www.imdb.com/title/tt1190634/episodes?season=2',
            'https://www.imdb.com/title/tt1190634/episodes?season=1',
            'https://www.imdb.com/title/tt1190634/fullcredits/'
        }
        urls = [
            "https://www.imdb.com/title/tt1190634/",
            "https://www.imdb.com/title/tt1190634/episodes?season=1",
            "https://www.imdb.com/title/tt1190634/episodes?season=2",
            "https://www.imdb.com/title/tt1190634/fullcredits/",
            "https://www.imdb.com/title/tt1190634/ratings/",
            "https://www.rottentomatoes.com/tv/the_boys_2019/",
        ]

        result = self.get_scrapper_result(urls=urls, search_type=Series.TYPE)

        self.assertTrue(self.is_subset(attrs=series_expected_attrs, results=result))

    def test__lotr(self):
        movies_expected_attrs = {
            'https://www.rottentomatoes.com/m/the_lord_of_the_rings_the_fellowship_of_the_ring/',
            'https://www.imdb.com/title/tt0120737/ratings/',
            'https://www.imdb.com/title/tt0120737/awards/',
            'https://www.imdb.com/title/tt0120737/',
            'https://www.imdb.com/title/tt0120737/fullcredits/'
        }
        urls = [
            "https://www.imdb.com/title/tt0120737/",
            "https://www.imdb.com/title/tt0120737/fullcredits/",
            "https://www.rottentomatoes.com/m/the_lord_of_the_rings_the_fellowship_of_the_ring/",
        ]

        result = self.get_scrapper_result(urls=urls, search_type=Movie.TYPE)

        self.assertTrue(self.is_subset(attrs=movies_expected_attrs, results=result))
