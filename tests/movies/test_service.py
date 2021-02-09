from tests.collector.base_test import BaseTest
from TvFY.collector.base import Scrapper
from TvFY.collector.google import GoogleScrapper
from TvFY.movies.models import Movie, MovieCast
from TvFY.movies.service import MovieCastService, MovieService


class TestMovieServices(BaseTest):
    def test_complete_movie(self):
        cls = GoogleScrapper(search_key="the dark knight")
        google_result = cls.run()
        urls = [
            "https://www.imdb.com/title/tt0120737/",
            "https://www.imdb.com/title/tt0120737/fullcredits",
            "https://www.imdb.com/title/tt0120737/awards",
            "https://www.rottentomatoes.com/m/the_lord_of_the_rings_the_fellowship_of_the_ring",  # noqa
        ]
        cls = Scrapper(urls=urls, search_type=self.movie)
        result = cls.handle()
        result.update(google_result)

        movie_cls = MovieService(search_data=result)
        movie = movie_cls.create_movie()

        movie_cast_cls = MovieCastService(search_data=result, movie=movie)
        movie_cast_cls.create_movie_cast()

        movie = Movie.objects.prefetch_related(
            "genres", "country", "language"
        ).select_related("director")
        movie_cast = MovieCast.objects.select_related("movie", "actor")

        self.assertTrue(movie)
        self.assertTrue(movie_cast)

        movie = movie.first()
        self.assertTrue(movie.name)
        self.assertEqual(movie.run_time, 178)
        self.assertTrue(movie.storyline)
        self.assertTrue(movie.director.get_full_name)
        self.assertTrue(movie.director.imdb_url)
        self.assertTrue(movie.director.rt_url)
        self.assertTrue(movie.genres.first())
        self.assertTrue(movie.country.first())
        self.assertTrue(movie.language.first())

        movie_cast = movie_cast.first()
        self.assertTrue(movie_cast.character_name)
        self.assertTrue(movie_cast.movie.name)
        self.assertTrue(movie_cast.actor.first_name)
