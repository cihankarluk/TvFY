from tests.base.test_base import BaseCollectorTest
from TvFY.collector.base import Scrapper


class RTSeriesTestCase(BaseCollectorTest):
    def test_the_boys(self):
        urls = ["https://www.rottentomatoes.com/tv/the_boys_2019"]
        cls = Scrapper(urls=urls, search_type=self.series)
        result = cls.handle()

        self.rt_control_home_page(result)

    def test_the_seven_deadly_sins(self):
        urls = ["https://www.rottentomatoes.com/tv/the_seven_deadly_sins"]
        cls = Scrapper(urls, search_type=self.series)
        result = cls.handle()

        self.assertTrue(result["network"])
        self.assertTrue(result["rt_genre"])
        self.assertTrue(result["storyline"])

    def test_the_expanse(self):
        urls = ["https://www.rottentomatoes.com/tv/the_expanse"]
        cls = Scrapper(urls=urls, search_type=self.series)
        result = cls.handle()

        self.rt_control_home_page(result)


class RTMoviesTestCase(BaseCollectorTest):
    def test_lotr_fellowship_of_the_ring(self):
        urls = [
            "https://www.rottentomatoes.com/m/the_lord_of_the_rings_the_fellowship_of_the_ring"  # noqa
        ]
        cls = Scrapper(urls, search_type=self.movie)
        result = cls.handle()

        self.rt_control_home_page_movie(result=result)

    def test_the_dark_knight(self):
        urls = ["https://www.rottentomatoes.com/m/the_dark_knight"]
        cls = Scrapper(urls, search_type=self.movie)
        result = cls.handle()

        self.rt_control_home_page_movie(result=result)
