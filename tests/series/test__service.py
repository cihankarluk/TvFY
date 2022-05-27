from unittest.mock import patch

from TvFY.actor.service import ActorService
from TvFY.core.exceptions import NotAbleToFindSeriesSourceUrl
from TvFY.series.models import Series, SeriesCast
from TvFY.series.service import SeriesService, SeriesCastService
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
        self.assertEqual(2, series.language.count())
        self.assertEqual(2, series.country.count())
        self.assertEqual(4, series.genres.count())

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
            "imdb_genre",
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
                    self.assertEqual(2, attribute.count())
            except AttributeError:
                attribute_errors.add(key)
        self.assertFalse(expected_attribute_errors - attribute_errors)
        self.assertEqual(4, series.genres.count())

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

    @patch.object(ActorService, "create_multiple_actor")
    def test__bulk_create_series_cast__empty_cast(self, mock_create_multiple_actor):
        mock_create_multiple_actor.return_value = {}
        search_data = {}

        SeriesCastService.bulk_create_series_cast(search_data=search_data, series=self.series)

        series_cast_query = SeriesCast.objects.all()
        self.assertEqual(0, series_cast_query.count())

    @patch.object(ActorService, "create_multiple_actor")
    def test__bulk_create_series_cast(self, mock_create_multiple_actor):
        actors = self.create_actor()
        mock_create_multiple_actor.return_value = {
            "https://t.com/1/": {"actor": actors[0]},
            "https://t.com/2/": {"actor": actors[1]},
        }
        search_data = {
            "cast": [
                {
                    "first_name": "Karl",
                    "last_name": "Urban",
                    "character_name": "The Butcher",
                    "imdb_actor_url": "https://t.com/1/",
                    "episode_count": 24,
                    "start_acting": self.now,
                    "end_acting": self.now,
                },
                {
                    "first_name": "Mahmut",
                    "last_name": "Tuncer",
                    "character_name": "The Halay",
                    "imdb_actor_url": "https://t.com/2/",
                    "episode_count": 24,
                    "start_acting": self.now,
                    "end_acting": self.now,
                },
            ]
        }

        SeriesCastService.bulk_create_series_cast(search_data=search_data, series=self.series)

        series_cast_query = SeriesCast.objects.all()
        self.assertEqual(2, series_cast_query.count())
