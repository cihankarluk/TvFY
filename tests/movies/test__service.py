from unittest.mock import patch

from TvFY.actor.service import ActorService
from TvFY.director.service import DirectorService
from TvFY.movies.models import MovieCast, Movie
from TvFY.movies.service import MovieService, MovieCastService
from tests.base import BaseTestCase


class MovieServiceTestCase(BaseTestCase):
    def setUp(self) -> None:
        super(MovieServiceTestCase, self).setUp()
        self.search_data = self.read_file("movie_batman.json", is_json=True)
        self.updated_search_data = self.read_file("movie_batman_updated.json", is_json=True)

    def test__prepare_movie_data(self):
        expected_attrs = {
            'imdb_genre',
            'imdb_director',
            'imdb_director_url',
            'run_time',
            'imdb_popularity',
            'country',
            'language',
            'release_date',
            'imdb_title',
            'budget_amount',
            'budget_currency',
            'usa_ow_amount',
            'usa_ow_currency',
            'ww_amount',
            'ww_currency',
            'metacritic_score',
            'imdb_vote_count',
            'imdb_rate',
            'wins',
            'nominations',
            'oscar_wins',
            'oscar_nominations',
            'cast',
            'imdb_url',
            'rt_title',
            'rt_genre',
            'rt_director',
            'rt_director_url',
            'rt_audience_rate',
            'rt_audience_count',
            'rt_tomatometer_rate',
            'rt_tomatometer_count',
            'rt_storyline',
            'rotten_tomatoes_url'
        }

        result = MovieService.prepare_movie_data(search_data=self.search_data)

        self.assertTrue(self.is_subset(attrs=expected_attrs, results=result))

    def test__get_movie__imdb_url(self):
        movie = self.create_movie()[0]

        result = MovieService.get_movie(filter_map={"imdb_url": movie.imdb_url})

        self.assertEqual(movie, result)

    def test__get_movie__rotten_tomatoes_url(self):
        movie = self.create_movie()[0]

        result = MovieService.get_movie(filter_map={"rotten_tomatoes_url": movie.rotten_tomatoes_url})

        self.assertEqual(movie, result)

    def test__get_movie__none(self):
        result = MovieService.get_movie(filter_map={"imdb_url": "wrong_url"})

        self.assertIsNone(result)

    def test__check_movie_exists__imdb_url(self):
        movie = self.create_movie()[0]
        movie_data = {"imdb_url": movie.imdb_url}

        result = MovieService.check_movie_exists(movie_data=movie_data)

        self.assertEqual(movie, result)

    def test__check_movie_exists__rotten_tomatoes_url(self):
        movie = self.create_movie()[0]
        movie_data = {"rotten_tomatoes_url": movie.rotten_tomatoes_url}

        result = MovieService.check_movie_exists(movie_data=movie_data)

        self.assertEqual(movie, result)

    def test__check_movie_exists__not_exists(self):
        movie_data = {}

        result = MovieService.check_movie_exists(movie_data=movie_data)

        self.assertIsNone(result)

    def test__create_movie_model_data(self):
        expected_attrs = {
            "title",
            "storyline",
            "release_date",
            "run_time",
            "imdb_popularity",
            "imdb_rate",
            "imdb_vote_count",
            "wins",
            "nominations",
            "oscar_wins",
            "oscar_nominations",
            "budget_amount",
            "budget_currency",
            "usa_ow_amount",
            "usa_ow_currency",
            "ww_amount",
            "ww_currency",
            "metacritic_score",
            "rt_tomatometer_rate",
            "rt_tomatometer_count",
            "rt_audience_rate",
            "rt_audience_count",
            "imdb_url",
            "rotten_tomatoes_url",
            "director",
        }
        movie_data = MovieService.prepare_movie_data(self.search_data)

        result = MovieService.create_movie_model_data(movie_data=movie_data)

        self.assertTrue(self.is_subset(attrs=expected_attrs, results=result))

    @patch.object(DirectorService, "get_or_create_director")
    def test__update_movie(self, mock_get_or_create_director):
        mock_get_or_create_director.return_value = self.create_director(count=1)[0]
        movie_data = {"imdb_title": "The Batman", "imdb_rate": 7.9}
        movie = self.create_movie()[0]

        updated_movie = MovieService.update_movie(movie=movie, movie_data=movie_data)

        self.assertEqual(movie.tvfy_code, updated_movie.tvfy_code)
        self.assertEqual("The Batman", updated_movie.title)
        self.assertEqual(7.9, updated_movie.imdb_rate)

    def test__create_movie(self):
        movie_data = MovieService.prepare_movie_data(search_data=self.search_data)

        MovieService.create_movie(movie_data=movie_data)

        movie_query = Movie.objects.filter(title="Batman Begins")
        self.assertTrue(movie_query.exists())
        movie = movie_query.get()
        self.assertEqual(2, movie.language.count())
        self.assertEqual(2, movie.country.count())
        self.assertEqual(5, movie.genres.count())

    def test__create_or_update_movie__create_movie(self):
        expected_attribute_errors = {
            'cast',
            'imdb_director',
            'imdb_director_url',
            'imdb_genre',
            'imdb_title',
            'release_date',
            'rt_director',
            'rt_director_url',
            'rt_genre',
            'rt_storyline',
            'rt_title',
        }
        movie_data = MovieService.prepare_movie_data(search_data=self.search_data)

        MovieService.create_or_update_movie(search_data=self.search_data)

        movie_query = Movie.objects.filter(title=self.search_data[self.search_data["imdb_url"]]["imdb_title"])
        self.assertTrue(movie_query.exists())
        movie = movie_query.get()
        attribute_errors = set()
        for key, value in movie_data.items():
            try:
                attribute = getattr(movie, key)
                if isinstance(attribute, (str, int, float)):
                    self.assertEqual(attribute, value)
                else:
                    # Country and Language
                    self.assertEqual(2, attribute.count())
            except AttributeError:
                attribute_errors.add(key)

        self.assertFalse(expected_attribute_errors - attribute_errors)
        self.assertFalse(attribute_errors - expected_attribute_errors)
        self.assertEqual(5, movie.genres.count())

    def test__create_or_update_movie__update_movie(self):
        """
        wins is increased from 121 to 420
        """
        MovieService.create_or_update_movie(search_data=self.search_data)
        initial_movie = Movie.objects.get(imdb_url=self.search_data["imdb_url"])

        MovieService.create_or_update_movie(search_data=self.updated_search_data)
        updated_movie = Movie.objects.get(imdb_url=self.search_data["imdb_url"])

        self.assertNotEqual(initial_movie.wins, updated_movie.wins)
        self.assertEqual(420, updated_movie.wins)


class MovieCastServiceTestCase(BaseTestCase):
    def setUp(self) -> None:
        super(MovieCastServiceTestCase, self).setUp()
        self.movie = self.create_movie()[0]

    @patch.object(ActorService, "create_multiple_actor")
    def test__bulk_create_movie_cast__empty_cast(self, mock_create_multiple_actor):
        mock_create_multiple_actor.return_value = {}
        movie_data = {}

        MovieCastService.bulk_create_movie_cast(movie=self.movie, movie_data=movie_data)

        movie_cast_query = MovieCast.objects.all()
        self.assertEqual(0, movie_cast_query.count())

    @patch.object(ActorService, "create_multiple_actor")
    def test__bulk_create_movie_cast(self, mock_create_multiple_actor):
        actors = self.create_actor()
        mock_create_multiple_actor.return_value = {
            "https://t.com/1/": {"actor": actors[0]},
            "https://t.com/2/": {"actor": actors[1]},
        }
        movie_data = {
            "cast": [
                {"first_name": "K", "last_name": "U", "character_name": "B", "imdb_actor_url": "https://t.com/1/"},
                {"first_name": "M", "last_name": "T", "character_name": "H", "imdb_actor_url": "https://t.com/2/"},
            ]
        }

        MovieCastService.bulk_create_movie_cast(movie=self.movie, movie_data=movie_data)

        movie_cast_query = MovieCast.objects.all()
        self.assertEqual(2, movie_cast_query.count())
