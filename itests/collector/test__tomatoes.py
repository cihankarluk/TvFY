from itests.base import BaseTestCase
from TvFY.collector.base import Scraper
from TvFY.movies.models import Movie
from TvFY.series.models import Series


class TomatoesBaseTestCase(BaseTestCase):
    def test__movie1(self):
        expected_attrs = {
            "rt_genre",
            "rt_director",
            "rt_director_url",
            "rt_audience_rate",
            "rt_audience_count",
            "rt_tomatometer_rate",
            "rt_tomatometer_count",
            "rt_title",
        }
        urls = [
            "https://www.rottentomatoes.com/m/the_lord_of_the_rings_the_fellowship_of_the_ring",
        ]

        result = Scraper(urls=urls, search_type=Movie.TYPE).handle()

        for url in urls:
            self.assertListEqual([], self.take_diff(attrs=expected_attrs, results=result[url]))

    def test__series1(self):
        expected_attrs = {
            "rt_genre",
            "rt_audience_rate",
            "rt_tomatometer_rate",
            "tv_network",
        }
        urls = [
            "https://www.rottentomatoes.com/tv/the_office",
        ]

        result = Scraper(urls=urls, search_type=Series.TYPE).handle()

        for url in urls:
            self.assertListEqual([], self.take_diff(attrs=expected_attrs, results=result[url]))
