from django.urls import reverse

from tests.base import BaseTestCase
from TvFY.movies.service import MovieService


class MovieViewSetTestCase(BaseTestCase):
    movie_list_url = reverse("movie-list")

    def setUp(self) -> None:
        super(MovieViewSetTestCase, self).setUp()
        movie_data = self.read_file("movie_lotr.json", is_json=True)

        MovieService(search_data=movie_data).create_movie()

    def test__list(self):
        expected_attrs = [
            "id",
            "tvfy_code",
            "title",
            "storyline",
            "release_date",
            "run_time",
            "rt_tomatometer_rate",
            "rt_audience_rate",
            "imdb_popularity",
            "imdb_rate",
            "imdb_vote_count",
            "wins",
            "nominations",
            "budget",
            "budget_currency",
            "usa_opening_weekend",
            "usa_opening_weekend_currency",
            "ww_gross",
            "imdb_url",
            "rotten_tomatoes_url",
            "director",
            "genres",
            "country",
            "language",
        ]
        response = self.client.get(self.movie_list_url)
        json_response = response.json()

        self.assertEqual(response.status_code, 200)
        self.is_subset(attrs=expected_attrs, results=json_response["results"])
