from tests.base import BaseTestCase
from TvFY.movies.service import MovieService


class MovieServiceTestCase(BaseTestCase):
    def test__create_movie(self):
        result = self.read_file("movie_lotr.json", is_json=True)

        movie = MovieService(search_data=result).create_movie()

        self.assertIsNotNone(movie.title)
        self.assertIsNotNone(movie.storyline)
        self.assertIsNotNone(movie.release_date)
        self.assertIsNotNone(movie.run_time)
        self.assertIsNotNone(movie.rt_tomatometer_rate)
        self.assertIsNotNone(movie.rt_audience_rate)
        self.assertIsNotNone(movie.imdb_popularity)
        self.assertIsNotNone(movie.imdb_rate)
        self.assertIsNotNone(movie.imdb_vote_count)
        self.assertIsNotNone(movie.wins)
        self.assertIsNotNone(movie.nominations)
        self.assertIsNotNone(movie.budget)
        self.assertIsNotNone(movie.budget_currency)
        self.assertIsNotNone(movie.usa_opening_weekend)
        self.assertIsNotNone(movie.usa_opening_weekend_currency)
        self.assertIsNotNone(movie.ww_gross)
        self.assertIsNotNone(movie.imdb_url)
        self.assertIsNotNone(movie.rotten_tomatoes_url)
        self.assertIsNotNone(movie.director)
        self.assertEqual(movie.genres.count(), 4)
        self.assertEqual(movie.country.count(), 2)
        self.assertEqual(movie.language.count(), 2)
        self.assertEqual(movie.moviecast_set.count(), 135)
