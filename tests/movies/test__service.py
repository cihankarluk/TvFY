from unittest.mock import patch

from TvFY.actor.service import ActorService
from TvFY.core.exceptions import NotAbleToFindMovieSourceUrl
from TvFY.movies.models import MovieCast, Movie
from TvFY.movies.service import MovieService, MovieCastService
from tests.base import BaseTestCase


class MovieServiceTestCase(BaseTestCase):
    def setUp(self) -> None:
        super(MovieServiceTestCase, self).setUp()
        self.expected_attribute_errors = {
            "rt_genre",
            "imdb_genre",
            "rt_director",
            "rt_director_url",
            "imdb_director",
            "imdb_director_url",
            "cast",
        }
        self.movie_data = self.read_file("movie_lotr.json", is_json=True)
        self.updated_movie_data = self.read_file("movie_lotr_updated.json", is_json=True)

    def test__check_source_urls(self):
        """
        Expect to not raise any errors.
        """
        search_data = {"imdb_url": "test"}
        result = MovieService.check_source_urls(search_data=search_data)
        self.assertIsNone(result)

        search_data = {"rotten_tomatoes_url": "test"}
        result = MovieService.check_source_urls(search_data=search_data)
        self.assertIsNone(result)

        search_data = {"imdb_url": "test", "rotten_tomatoes_url": "test"}
        result = MovieService.check_source_urls(search_data=search_data)
        self.assertIsNone(result)

    def test__check_source_url__raise_NotAbleToFindMovieSourceUrl(self):
        search_data = {}
        with self.assertRaises(NotAbleToFindMovieSourceUrl):
            MovieService.check_source_urls(search_data=search_data)

    def test__get_movie__imdb_url(self):
        movie = self.create_movie()[0]

        result = MovieService.get_movie(key="imdb_url", url=movie.imdb_url)

        self.assertEqual(movie, result)

    def test__get_movie__rotten_tomatoes_url(self):
        movie = self.create_movie()[0]

        result = MovieService.get_movie(key="rotten_tomatoes_url", url=movie.rotten_tomatoes_url)

        self.assertEqual(movie, result)

    def test__get_movie__none(self):
        result = MovieService.get_movie(key="imdb_url", url="wrong_url")

        self.assertIsNone(result)

    def test__check_movie_exists__imdb_url(self):
        movie = self.create_movie()[0]
        search_data = {"imdb_url": movie.imdb_url}

        result = MovieService.check_movie_exists(search_data=search_data)

        self.assertEqual(movie, result)

    def test__check_movie_exists__rotten_tomatoes_url(self):
        movie = self.create_movie()[0]
        search_data = {"rotten_tomatoes_url": movie.rotten_tomatoes_url}

        result = MovieService.check_movie_exists(search_data=search_data)

        self.assertEqual(movie, result)

    def test__check_movie_exists__not_exists(self):
        search_data = {}

        result = MovieService.check_movie_exists(search_data=search_data)

        self.assertIsNone(result)

    def test__create_movie(self):
        movie_data = {"title": "The Lord of the Rings: The Fellowship of the Ring"}
        MovieService.create_movie(movie_data=movie_data, search_data=self.movie_data)

        movie_query = Movie.objects.filter(title="The Lord of the Rings: The Fellowship of the Ring")
        self.assertTrue(movie_query.exists())
        movie = movie_query.get()
        self.assertEqual(2, movie.language.count())
        self.assertEqual(2, movie.country.count())
        self.assertEqual(4, movie.genres.count())

    def test__update_movie(self):
        movie_data = {"title": "The Batman", "imdb_rate": 7.9}
        movie = self.create_movie()[0]

        updated_movie = MovieService.update_movie(movie=movie, movie_data=movie_data)

        self.assertEqual(movie.tvfy_code, updated_movie.tvfy_code)
        self.assertEqual("The Batman", updated_movie.title)
        self.assertEqual(7.9, updated_movie.imdb_rate)

    def test__create_or_update_movie__create_movie(self):
        MovieService.create_or_update_movie(search_data=self.movie_data)

        movie_query = Movie.objects.filter(title="The Lord of the Rings: The Fellowship of the Ring")
        self.assertTrue(movie_query.exists())
        movie = movie_query.get()
        attribute_errors = set()
        for key, value in self.movie_data.items():
            try:
                attribute = getattr(movie, key)
                if isinstance(attribute, str):
                    self.assertEqual(attribute, value)
                elif isinstance(attribute, int):
                    self.assertEqual(attribute, int(value))
                else:
                    # Country and Language
                    self.assertEqual(2, attribute.count())
            except AttributeError:
                attribute_errors.add(key)
        self.assertFalse(self.expected_attribute_errors - attribute_errors)
        self.assertEqual(4, movie.genres.count())

    def test__create_or_update_movie__update_movie(self):
        """
        wins is increased from 121 to 420
        """
        MovieService.create_or_update_movie(search_data=self.movie_data)
        initial_movie = Movie.objects.get(imdb_url=self.movie_data["imdb_url"])

        MovieService.create_or_update_movie(search_data=self.updated_movie_data)
        updated_movie = Movie.objects.get(imdb_url=self.movie_data["imdb_url"])

        self.assertNotEqual(initial_movie.wins, updated_movie.wins)
        self.assertEqual(420, updated_movie.wins)


class MovieCastServiceTestCase(BaseTestCase):
    def setUp(self) -> None:
        super(MovieCastServiceTestCase, self).setUp()
        self.movie = self.create_movie()[0]

    @patch.object(ActorService, "create_multiple_actor")
    def test__bulk_create_movie_cast__empty_cast(self, mock_create_multiple_actor):
        mock_create_multiple_actor.return_value = {}
        search_data = {}

        MovieCastService.bulk_create_movie_cast(search_data=search_data, movie=self.movie)

        movie_cast_query = MovieCast.objects.all()
        self.assertEqual(0, movie_cast_query.count())

    @patch.object(ActorService, "create_multiple_actor")
    def test__bulk_create_movie_cast(self, mock_create_multiple_actor):
        actors = self.create_actor()
        mock_create_multiple_actor.return_value = {
            "https://t.com/1/": {"actor": actors[0]},
            "https://t.com/2/": {"actor": actors[1]},
        }
        search_data = {
            "cast": [
                {"first_name": "K", "last_name": "U", "character_name": "The Butcher", "imdb_actor_url": "https://t.com/1/"},
                {"first_name": "M", "last_name": "T", "character_name": "The Halay", "imdb_actor_url": "https://t.com/2/"},
            ]
        }

        MovieCastService.bulk_create_movie_cast(search_data=search_data, movie=self.movie)

        movie_cast_query = MovieCast.objects.all()
        self.assertEqual(2, movie_cast_query.count())
