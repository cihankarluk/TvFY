from itests.base import BaseTestCase
from TvFY.series.models import Season
from TvFY.series.service import SeriesSeasonEpisodeService


class SeriesSeasonEpisodeServiceTestCase(BaseTestCase):
    def test__scrap_and_update_episodes(self):
        series1 = self.create_series(season_count=3, imdb_url="https://www.imdb.com/title/tt1190634/")
        self.create_season(
            season=1,
            series=series1,
            imdb_url="https://www.imdb.com/title/tt1190634/?season=1",
        )

        SeriesSeasonEpisodeService.scrap_and_update_episodes()

        episode_query = Season.objects.get(season=2).episode_set.all()
        self.assertEqual(8, episode_query.count())
