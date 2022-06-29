from TvFY.core.exceptions import MovieNotFoundError
from TvFY.user.models import UserMovies, UserSeries
from TvFY.user.service import UserService
from tests.base import BaseTestCase


class UserServiceTestCase(BaseTestCase):

    def test__create_or_update_user_movie__create(self):
        movie = self.create_movie(count=1)[0]
        request_data = {
            "tvfy_code": movie.tvfy_code,
            "is_watched": True,
            "is_going_to_watch": False,
        }

        result = UserService.create_or_update_user_movie(user=self.account, request_data=request_data)

        user_movie = UserMovies.objects.get(user=self.account, movie=movie)
        self.assertEqual(user_movie, result)

    def test__create_or_update_user_movie__update(self):
        user_movie = self.create_user_movies(count=1)[0]
        request_data = {
            "tvfy_code": user_movie.movie.tvfy_code,
            "is_watched": False,
            "is_going_to_watch": True,
        }

        result = UserService.create_or_update_user_movie(user=self.account, request_data=request_data)

        updated_user_movie = UserMovies.objects.get(user=self.account, movie=user_movie.movie)
        self.assertNotEqual(user_movie.is_watched, updated_user_movie.is_watched)
        self.assertNotEqual(user_movie.is_going_to_watch, updated_user_movie.is_going_to_watch)
        self.assertEqual(updated_user_movie, result)

    def test__create_or_update_user_movie__raise_error(self):
        request_data = {
            "tvfy_code": "notExists",
            "is_watched": False,
            "is_going_to_watch": True,
        }

        with self.assertRaises(MovieNotFoundError):
            UserService.create_or_update_user_movie(user=self.account, request_data=request_data)

    def test__get_movies(self):
        expected_attrs = {
            "max_imdb_rate",
            "min_imdb_rate",
            "avg_imdb_rate",
            "max_rt_audience_rate",
            "min_rt_audience_rate",
            "avg_rt_audience_rate",
            "max_rt_tomatometer_rate",
            "min_rt_tomatometer_rate",
            "avg_rt_tomatometer_rate",
            "max_metacritic_score",
            "min_metacritic_score",
            "avg_metacritic_score",
            "newest_movie_watched",
            "oldest_movie_watched",
            "time_spent",
            "genres",
            "countries",
            "languages",
            "watched_movies",
            "watch_list",
        }
        _ = self.create_user_movies(count=1)
        _ = self.create_user_movies(count=1, index_start=2, is_watched=False, is_going_to_watch=True)

        result = UserService.get_movies(self.account)

        self.assertTrue(self.is_subset(attrs=expected_attrs, results=result))

    def test__update_user_series(self):
        user_series = self.create_user_series(count=1)[0]
        request_data = {
            "is_watched": False,
            "is_going_to_watch": True,
        }

        UserService.update_user_series(user_series=user_series, last_watched_episode=10, request_data=request_data)

        user_series.refresh_from_db()
        self.assertEqual(10, user_series.last_watched_episode)
        self.assertEqual(False, user_series.is_watched)
        self.assertEqual(True, user_series.is_going_to_watch)

    def test__create_user_series(self):
        series = self.create_series(count=1)[0]
        season = self.create_season(count=1)[0]
        request_data = {
            "is_watched": False,
            "is_going_to_watch": True,
        }

        user_series = UserService.create_user_series(
            user=self.account,
            series=series,
            watched_season=season,
            last_watched_episode=10,
            request_data=request_data
        )

        us_query = UserSeries.objects.filter(user=self.account, series=series)
        self.assertTrue(us_query.exists())
        self.assertEqual(us_query.get(), user_series)

    def test__create_or_update_user_series__create(self):
        series = self.create_series(count=1)[0]
        _ = self.create_season(count=1, season="1", series=series)[0]
        request_data = {
            "tvfy_code": series.tvfy_code,
            "watched_season": 1,
            "last_watched_episode": 10,
            "watched_past_seasons": False,
            "is_watched": True,
            "is_going_to_watch": False,
        }

        user_series = UserService.create_or_update_user_series(user=self.account, request_data=request_data)[0]

        us_query = UserSeries.objects.filter(user=self.account, series=series)
        self.assertTrue(us_query.exists())
        self.assertEqual(us_query.get(), user_series)

    def test__create_or_update_user_series__update(self):
        series = self.create_series(count=1)[0]
        season = self.create_season(count=1, season="1", series=series)[0]
        user_series = self.create_user_series(
            count=1,
            user=self.account,
            series=series,
            watched_season=season,
            last_watched_episode=15,
        )[0]
        request_data = {
            "tvfy_code": series.tvfy_code,
            "watched_season": 1,
            "last_watched_episode": 10,
            "watched_past_seasons": False,
            "is_watched": True,
            "is_going_to_watch": False,
        }

        updated_user_series = UserService.create_or_update_user_series(user=self.account, request_data=request_data)[0]

        us_query = UserSeries.objects.filter(user=self.account, series=series)
        self.assertTrue(us_query.exists())
        self.assertEqual(us_query.get(), updated_user_series)
        self.assertNotEqual(user_series.last_watched_episode, updated_user_series.last_watched_episode)

    def test__create_or_update_user_series__create_multiple(self):
        series = self.create_series(count=1)[0]
        season1 = self.create_season(count=1, season="1", series=series)[0]
        _ = self.create_episode(season=season1)
        season2 = self.create_season(count=1, season="2", series=series, index_start=2)[0]
        _ = self.create_episode(count=1, index_start=2, season=season2)
        season3 = self.create_season(count=1, season="3", series=series, index_start=3)[0]
        _ = self.create_episode(count=1, index_start=3, season=season3)
        request_data = {
            "tvfy_code": series.tvfy_code,
            "watched_season": 3,
            "last_watched_episode": 10,
            "watched_past_seasons": True,
            "is_watched": True,
            "is_going_to_watch": False,
        }

        result = UserService.create_or_update_user_series(user=self.account, request_data=request_data)

        self.assertEqual(3, len(result))
        us_query = UserSeries.objects.filter(user=self.account, series=series, watched_season=season1)
        self.assertTrue(us_query.exists())
        us_query = UserSeries.objects.filter(user=self.account, series=series, watched_season=season2)
        self.assertTrue(us_query.exists())
        us_query = UserSeries.objects.filter(user=self.account, series=series, watched_season=season3)
        self.assertTrue(us_query.exists())

    def test__create_or_update_user_series__create_and_update_multiple(self):
        series = self.create_series(count=1)[0]
        season1 = self.create_season(count=1, season="1", series=series)[0]
        _ = self.create_episode(season=season1)
        season2 = self.create_season(count=1, season="2", series=series, index_start=2)[0]
        _ = self.create_episode(count=1, index_start=2, season=season2)
        season3 = self.create_season(count=1, season="3", series=series, index_start=3)[0]
        _ = self.create_episode(count=1, index_start=3, season=season3)

        us1 = self.create_user_series(
            count=1,
            user=self.account,
            series=series,
            watched_season=season1,
            last_watched_episode=15,
        )[0]
        us3 = self.create_user_series(
            count=1,
            user=self.account,
            series=series,
            watched_season=season3,
            last_watched_episode=21,
        )[0]
        request_data = {
            "tvfy_code": series.tvfy_code,
            "watched_season": 3,
            "last_watched_episode": 12,
            "watched_past_seasons": True,
            "is_watched": True,
            "is_going_to_watch": False,
        }

        result = UserService.create_or_update_user_series(user=self.account, request_data=request_data)

        self.assertEqual(3, len(result))
        us_query = UserSeries.objects.filter(user=self.account, series=series, watched_season=season1)
        self.assertTrue(us_query.exists())
        updated_us = us_query.get()
        self.assertEqual(10, updated_us.last_watched_episode)
        self.assertNotEqual(us1.last_watched_episode, updated_us.last_watched_episode)
        us_query = UserSeries.objects.filter(user=self.account, series=series, watched_season=season2)
        self.assertTrue(us_query.exists())
        updated_us = us_query.get()
        self.assertEqual(1, updated_us.last_watched_episode)
        us_query = UserSeries.objects.filter(user=self.account, series=series, watched_season=season3)
        self.assertTrue(us_query.exists())
        updated_us = us_query.get()
        self.assertEqual(12, updated_us.last_watched_episode)
        self.assertNotEqual(us3.last_watched_episode, updated_us.last_watched_episode)

    def test__get_user_series(self):
        expected_attrs = {
            "last_watched_episode",
            "series",
            "watched_seasons",
            "unwatched_seasons",
        }
        user_series = self.create_user_series(count=1, last_watched_episode=10)[0]

        results = UserService.get_user_series(user=self.account)

        self.assertTrue(self.is_subset(attrs=expected_attrs, results=results))
        self.assertEqual(user_series.series, results[0]["series"])
        self.assertListEqual([user_series.watched_season], results[0]["watched_seasons"])
