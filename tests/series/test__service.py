from TvFY.core.exceptions import NotAbleToFindSeriesSourceUrl
from TvFY.series.models import Series, SeriesCast, Episode, Season
from TvFY.series.service import SeriesService, SeriesCastService, SeriesSeasonEpisodeService
from tests.base import BaseTestCase


class SeriesServiceTestCase(BaseTestCase):

    def setUp(self) -> None:
        super(SeriesServiceTestCase, self).setUp()
        self.search_data = self.read_file("series_the_boys.json", is_json=True)
        self.updated_search_data = self.read_file("series_the_boys_updated.json", is_json=True)

    def test__check_source_urls(self):
        """
        Expect to not raise any errors.
        """
        search_data = {"imdb_url": "test"}
        result = SeriesService.check_source_urls(search_data=search_data)
        self.assertIsNone(result)

        search_data = {"rotten_tomatoes_url": "test"}
        result = SeriesService.check_source_urls(search_data=search_data)
        self.assertIsNone(result)

        search_data = {"imdb_url": "test", "rotten_tomatoes_url": "test"}
        result = SeriesService.check_source_urls(search_data=search_data)
        self.assertIsNone(result)

    def test__check_source_url__raise_NotAbleToFindMovieSourceUrl(self):
        search_data = {}
        with self.assertRaises(NotAbleToFindSeriesSourceUrl):
            SeriesService.check_source_urls(search_data=search_data)

    def test__get_series__imdb_url(self):
        series = self.create_series()[0]

        result = SeriesService.get_series(filter_map={"imdb_url": series.imdb_url})

        self.assertEqual(series, result)

    def test__get_series__rotten_tomatoes_url(self):
        series = self.create_series()[0]

        result = SeriesService.get_series(filter_map={"rotten_tomatoes_url": series.rotten_tomatoes_url})

        self.assertEqual(series, result)

    def test__get_series__none(self):
        result = SeriesService.get_series(filter_map={"imdb_url": "wrong_url"})

        self.assertIsNone(result)

    def test__check_series_exists__imdb_url(self):
        series = self.create_series()[0]
        search_data = {"imdb_url": series.imdb_url}

        result = SeriesService.check_series_exists(search_data=search_data)

        self.assertEqual(series, result)

    def test__check_series_exists__rotten_tomatoes_url(self):
        series = self.create_series()[0]
        search_data = {"rotten_tomatoes_url": series.rotten_tomatoes_url}

        result = SeriesService.check_series_exists(search_data=search_data)

        self.assertEqual(series, result)

    def test__check_series_exists__not_exists(self):
        search_data = {}

        result = SeriesService.check_series_exists(search_data=search_data)

        self.assertIsNone(result)

    def test__create_series(self):
        series_data = {"title": "The Boys"}

        SeriesService.create_series(series_data=series_data, search_data=self.search_data)

        series_query = Series.objects.filter(title="The Boys")
        self.assertTrue(series_query.exists())
        series = series_query.get()
        self.assertEqual(1, series.language.count())
        self.assertEqual(1, series.country.count())
        self.assertEqual(1, series.genres.count())

        series_cast_query = SeriesCast.objects.all()
        self.assertEqual(4, series_cast_query.count())
        series_episode_query = Episode.objects.all()
        self.assertEqual(8, series_episode_query.count())

    def test__update_series(self):
        series_data = {"title": "The Boys", "imdb_rate": 8.7}
        series = self.create_series()[0]

        updated_series = SeriesService.update_series(series=series, series_data=series_data)

        self.assertEqual(series.tvfy_code, updated_series.tvfy_code)
        self.assertEqual("The Boys", updated_series.title)
        self.assertEqual(8.7, updated_series.imdb_rate)

    def test__create_or_update_series__create_series(self):
        expected_attribute_errors = {
            "rt_genre",
            "imdb_director",
            "imdb_director_url",
            "cast",
        }
        SeriesService.create_or_update_series(search_data=self.search_data)

        series_query = Series.objects.filter(title="The Boys")
        self.assertTrue(series_query.exists())
        series = series_query.get()
        attribute_errors = set()
        for key, value in self.search_data.items():
            try:
                attribute = getattr(series, key)
                if isinstance(attribute, str):
                    self.assertEqual(attribute, value)
                elif isinstance(attribute, int):
                    self.assertEqual(attribute, int(value))
                else:
                    # Country and Language
                    self.assertEqual(1, attribute.count())
            except AttributeError:
                attribute_errors.add(key)
        self.assertFalse(expected_attribute_errors - attribute_errors)
        self.assertEqual(1, series.genres.count())

    def test__create_or_update_movie__update_movie(self):
        """
        wins is increased from 8 to 420
        """
        SeriesService.create_or_update_series(search_data=self.search_data)
        initial_series = Series.objects.get(imdb_url=self.search_data["imdb_url"])

        SeriesService.create_or_update_series(search_data=self.updated_search_data)
        updated_series = Series.objects.get(imdb_url=self.search_data["imdb_url"])

        self.assertNotEqual(initial_series.wins, updated_series.wins)
        self.assertEqual(420, updated_series.wins)


class SeriesCastServiceTestCase(BaseTestCase):
    def setUp(self) -> None:
        super(SeriesCastServiceTestCase, self).setUp()
        self.series = self.create_series()[0]
        self.actor = self.create_actor()[0]
        self.search_data = self.read_file("series_the_boys.json", is_json=True)
        self.updated_search_data = self.read_file("series_the_boys_updated.json", is_json=True)

    def test__create_series_cast(self):
        cast_data = {
            "character_name": "The Butcher",
            "episode_count": 12,
        }

        result = SeriesCastService.create_series_cast(series=self.series, actor=self.actor, cast_data=cast_data)

        self.assertEqual("The Butcher", result.character_name)
        self.assertEqual(12, result.episode_count)
        self.assertEqual(self.actor, result.actor)
        self.assertEqual(self.series, result.series)

    def test__update_series_cast(self):
        cast_data = {
            "character_name": "The Butcher",
            "episode_count": 12,
        }
        series_cast = self.create_series_cast(index_start=100, count=1)[0]

        SeriesCastService.update_series_cast(series_cast=series_cast, cast_data=cast_data)

        series_cast.refresh_from_db()
        self.assertEqual("The Butcher", series_cast.character_name)
        self.assertEqual(12, series_cast.episode_count)

    def test__get_series_cast_query(self):
        cast_data_list = [
            {
                "character_name": "Test 1",
                "episode_count": 12,
            },
            {
                "character_name": "Test 2",
                "episode_count": 12,
            },
            {
                "character_name": "Test 3",
                "episode_count": 12,
            },
            {
                "character_name": "Test 4",
                "episode_count": 12,
            },
        ]
        actor_map = {
            "https://test1.com": "test1",
            "https://test2.com": "test2",
        }
        actor1 = self.create_actor(index_start=200, count=1, imdb_url="https://test1.com")[0]
        actor2 = self.create_actor(index_start=201, count=1, imdb_url="https://test2.com")[0]
        actor3 = self.create_actor(index_start=202, count=1, imdb_url="https://test3.com")[0]
        actor4 = self.create_actor(index_start=203, count=1, imdb_url="https://test4.com")[0]
        series1 = self.create_series(index_start=200, count=1)[0]

        self.create_series_cast(index_start=200, count=1, actor=actor1, series=series1, character_name="Test 1")
        self.create_series_cast(index_start=201, count=1, actor=actor2, series=series1)
        self.create_series_cast(index_start=202, count=1, actor=actor3, series=series1)
        self.create_series_cast(index_start=203, count=1, actor=actor4, series=self.series)

        result = SeriesCastService.get_series_cast_query(
            series=series1,
            cast_data_list=cast_data_list,
            actor_map=actor_map,
        )

        self.assertEqual(1, result.count())
        self.assertEqual("Test 1", result.first().character_name)

    def test__create_or_update_series_cast__empty_search_data(self):
        search_data = {}

        SeriesCastService.create_or_update_series_cast(series=self.series, search_data=search_data)

        series_cast_query = SeriesCast.objects.all()
        self.assertEqual(0, series_cast_query.count())

    def test__create_or_update_series_cast(self):
        SeriesCastService.create_or_update_series_cast(series=self.series, search_data=self.search_data)

        series_cast_query = SeriesCast.objects.all()
        self.assertEqual(4, series_cast_query.count())
        self.assertEqual(24, series_cast_query.first().episode_count)

        SeriesCastService.create_or_update_series_cast(series=self.series, search_data=self.updated_search_data)

        series_cast_query = SeriesCast.objects.all()
        self.assertEqual(4, series_cast_query.count())
        self.assertEqual(48, series_cast_query.first().episode_count)


class SeriesSeasonEpisodeServiceTestCase(BaseTestCase):
    def setUp(self) -> None:
        super(SeriesSeasonEpisodeServiceTestCase, self).setUp()
        self.series = self.create_series(count=1, season_count=1)[0]
        self.season = self.create_season(series=self.series, count=1)[0]
        self.episode = self.create_episode(season=self.season, count=1)[0]
        self.search_data = self.read_file("series_the_boys.json", is_json=True)
        self.updated_search_data = self.read_file("series_the_boys_updated.json", is_json=True)

    def test__create_episode(self):
        episode_data = {"title": "test1"}

        result = SeriesSeasonEpisodeService.create_episode(season=self.season, episode_data=episode_data)

        self.assertEqual("test1", result.title)

    def test__update_episode(self):
        episode_data = {"title": "test1"}

        self.assertEqual("None_0", self.episode.title)
        SeriesSeasonEpisodeService.update_episode(episode=self.episode, episode_data=episode_data)

        self.assertEqual("test1", self.episode.title)

    def test__get_episode_query(self):
        season_data = [
            {
                "title": "test1",
            },
        ]
        episode1 = self.create_episode(season=self.season, index_start=100, title="test1", count=1)[0]
        self.create_episode(season=self.season, index_start=110, title="test2", count=1)
        self.create_episode(season=self.create_season(index_start=120, count=1)[0], index_start=101, count=1)

        result = SeriesSeasonEpisodeService.get_episode_query(season=self.season, season_data=season_data)

        self.assertEqual(1, result.count())
        self.assertEqual(episode1, result.get())

    def test__create_or_update_series_season_episodes(self):
        SeriesSeasonEpisodeService.create_or_update_series_season_episodes(
            series=self.series, search_data=self.search_data, season_number="1",
        )

        season_query = Season.objects.filter(imdb_url="https://www.imdb.com/title/tt1190634/episodes?season=1")
        self.assertTrue(season_query.exists())
        episode_query = Episode.objects.filter(season=season_query.get())
        self.assertEqual(8, episode_query.count())
        self.assertEqual(8.7, episode_query.get(title="The Name of the Game").imdb_rate)
        self.assertEqual(8.5, episode_query.get(title="Cherry").imdb_rate)

        SeriesSeasonEpisodeService.create_or_update_series_season_episodes(
            series=self.series, search_data=self.updated_search_data, season_number="1",
        )

        season_query = Season.objects.filter(imdb_url="https://www.imdb.com/title/tt1190634/episodes?season=1")
        self.assertTrue(season_query.exists())
        episode_query = Episode.objects.filter(season=season_query.get())
        self.assertEqual(8, episode_query.count())
        self.assertEqual(9.7, episode_query.get(title="The Name of the Game").imdb_rate)
        self.assertEqual(9.5, episode_query.get(title="Cherry").imdb_rate)
