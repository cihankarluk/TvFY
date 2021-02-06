from TvFY.movies.helpers import SaveMovieData
from TvFY.collector.base import Scrapper
from TvFY.collector.google import GoogleScrapper

from tests.collector.base_test import BaseTest


class TestHelpers(BaseTest):
    def test_save_movie_data(self):
        cls = GoogleScrapper(search_key="lotr")
        google_result = cls.run()
        urls = [
            "https://www.imdb.com/title/tt0120737/",
            "https://www.imdb.com/title/tt0120737/fullcredits",
            "https://www.imdb.com/title/tt0120737/awards",
            "https://www.rottentomatoes.com/m/the_lord_of_the_rings_the_fellowship_of_the_ring" # noqa
        ]
        cls = Scrapper(urls=urls, search_type=self.movie)
        result = cls.handle()
        result.update(google_result)
        save = SaveMovieData(search_data=result)
        save.save_data()
