from tests.collector.base_test import BaseTest
from TvFY.collector.base import Scrapper
from TvFY.collector.google import GoogleScrapper
from TvFY.series.helpers import save_data
from TvFY.series.models import Episode, Season, Series, SeriesCast


class TestHelpers(BaseTest):
    def test_save_series_data(self):
        cls = GoogleScrapper(search_key="the boys")
        google_result = cls.run()
        urls = [
            "https://www.imdb.com/title/tt1190634/",
            "https://www.imdb.com/title/tt1190634/episodes?season=1",
            "https://www.imdb.com/title/tt1190634/episodes?season=2",
            "https://www.imdb.com/title/tt1190634/fullcredits",
            "https://www.imdb.com/title/tt1190634/awards",
            "https://www.rottentomatoes.com/tv/the_boys_2019",
        ]
        cls = Scrapper(urls=urls, search_type=self.series)
        result = cls.handle()
        result.update(google_result)
        save_data(result)

        series = Series.objects.prefetch_related("genres", "country", "language")
        series_cast = SeriesCast.objects.select_related("series", "actor")
        seasons = Season.objects.select_related("series")
        episodes = Episode.objects.select_related("season", "season__series")

        self.assertTrue(series)
        self.assertTrue(series_cast)
        self.assertTrue(seasons)
        self.assertTrue(episodes)

        series = series.first()
        self.assertEqual(series.name, "The Boys")
        self.assertEqual(series.run_time, 60)
        self.assertTrue(series.storyline)
        self.assertTrue(series.imdb_creator_url)
        self.assertTrue(series.genres.first())
        self.assertTrue(series.country.first())
        self.assertTrue(series.language.first())

        series_cast = series_cast.first()
        self.assertTrue(series_cast.character_name)
        self.assertEqual(series_cast.series.name, "The Boys")
        self.assertTrue(series_cast.actor.first_name)

        season = seasons.first()
        self.assertTrue(season.imdb_url)
        self.assertTrue(season.imdb_season_average_rate)
        self.assertEqual(season.series.name, "The Boys")

        episode = episodes.first()
        self.assertTrue(episode.name)
        self.assertTrue(episode.storyline)
        self.assertTrue(episode.season)
        self.assertEqual(episode.season.series.name, "The Boys")
