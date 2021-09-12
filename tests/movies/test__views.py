from datetime import timedelta

from django.urls import reverse
from django.utils import timezone
from model_bakery import baker

from tests.base import BaseTestCase
from TvFY.core.models import Country, Language
from TvFY.genre.models import Genre
from TvFY.movies.models import Movie
from TvFY.movies.service import MovieService


class MovieViewSetTestCase(BaseTestCase):
    movie_list_url = reverse("movie-list")

    def setUp(self) -> None:
        super(MovieViewSetTestCase, self).setUp()
        movie_data = self.read_file("movie_lotr.json", is_json=True)

        self.movie = MovieService(search_data=movie_data).create_movie()

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

    def test__list__filter_release_date_after(self):
        now_ = timezone.now()
        second_movie = baker.make(Movie, release_date=now_)

        response = self.client.get(
            self.movie_list_url,
            data={"release_date_after": (now_ - timedelta(days=1)).strftime("%Y-%m-%d")},
        )
        json_response = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(json_response["count"], 1)
        self.assertEqual(json_response["results"][0]["id"], second_movie.id)

    def test__list__filter_release_date_before(self):
        now_ = timezone.now()
        baker.make(Movie, release_date=now_)

        response = self.client.get(
            self.movie_list_url,
            data={"release_date_before": (now_ - timedelta(days=1)).strftime("%Y-%m-%d")},
        )
        json_response = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(json_response["count"], 1)
        self.assertEqual(json_response["results"][0]["id"], self.movie.id)

    def test__list__filter_run_time_min(self):
        baker.make(Movie, run_time=self.movie.run_time - 1)

        response = self.client.get(
            self.movie_list_url,
            data={"run_time_min": self.movie.run_time},
        )
        json_response = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(json_response["count"], 1)
        self.assertEqual(json_response["results"][0]["id"], self.movie.id)

    def test__list__filter_run_time_max(self):
        baker.make(Movie, run_time=self.movie.run_time + 1)

        response = self.client.get(
            self.movie_list_url,
            data={"run_time_max": self.movie.run_time},
        )
        json_response = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(json_response["count"], 1)
        self.assertEqual(json_response["results"][0]["id"], self.movie.id)

    def test__list__filter_rt_tomatometer_rate_min(self):
        baker.make(Movie, rt_tomatometer_rate=self.movie.rt_tomatometer_rate - 1)

        response = self.client.get(
            self.movie_list_url,
            data={"rt_tomatometer_rate_min": self.movie.rt_tomatometer_rate},
        )
        json_response = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(json_response["count"], 1)
        self.assertEqual(json_response["results"][0]["id"], self.movie.id)

    def test__list__filter_rt_tomatometer_rate_max(self):
        baker.make(Movie, rt_tomatometer_rate=self.movie.rt_tomatometer_rate + 1)

        response = self.client.get(
            self.movie_list_url,
            data={"rt_tomatometer_rate_max": self.movie.rt_tomatometer_rate},
        )
        json_response = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(json_response["count"], 1)
        self.assertEqual(json_response["results"][0]["id"], self.movie.id)

    def test__list__filter_rt_audience_rate_min(self):
        baker.make(Movie, rt_audience_rate=self.movie.rt_audience_rate - 1)

        response = self.client.get(
            self.movie_list_url,
            data={"rt_audience_rate_min": self.movie.rt_audience_rate},
        )
        json_response = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(json_response["count"], 1)
        self.assertEqual(json_response["results"][0]["id"], self.movie.id)

    def test__list__filter_rt_audience_rate_max(self):
        baker.make(Movie, rt_audience_rate=self.movie.rt_audience_rate + 1)

        response = self.client.get(
            self.movie_list_url,
            data={"rt_audience_rate_max": self.movie.rt_audience_rate},
        )
        json_response = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(json_response["count"], 1)
        self.assertEqual(json_response["results"][0]["id"], self.movie.id)

    def test__list__filter_imdb_rate_min(self):
        baker.make(Movie, imdb_rate=self.movie.imdb_rate - 0.1)

        response = self.client.get(
            self.movie_list_url,
            data={"imdb_rate_min": self.movie.imdb_rate},
        )
        json_response = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(json_response["count"], 1)
        self.assertEqual(json_response["results"][0]["id"], self.movie.id)

    def test__list__filter_imdb_rate_max(self):
        baker.make(Movie, imdb_rate=self.movie.imdb_rate + 0.1)

        response = self.client.get(
            self.movie_list_url,
            data={"imdb_rate_max": self.movie.imdb_rate},
        )
        json_response = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(json_response["count"], 1)
        self.assertEqual(json_response["results"][0]["id"], self.movie.id)

    def test__list__filter_imdb_rate_range(self):
        baker.make(Movie, imdb_rate=self.movie.imdb_rate + 0.2)

        response = self.client.get(
            self.movie_list_url,
            data={
                "imdb_rate_max": self.movie.imdb_rate + 0.1,
                "imdb_rate_min": self.movie.imdb_rate - 0.1,
            },
        )
        json_response = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(json_response["count"], 1)
        self.assertEqual(json_response["results"][0]["id"], self.movie.id)

    def test__list__filter_imdb_popularity_min(self):
        baker.make(Movie, imdb_popularity=self.movie.imdb_popularity - 1)

        response = self.client.get(
            self.movie_list_url,
            data={"imdb_popularity_min": self.movie.imdb_popularity},
        )
        json_response = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(json_response["count"], 1)
        self.assertEqual(json_response["results"][0]["id"], self.movie.id)

    def test__list__filter_imdb_popularity_max(self):
        baker.make(Movie, imdb_popularity=self.movie.imdb_popularity + 1)

        response = self.client.get(
            self.movie_list_url,
            data={"imdb_popularity_max": self.movie.imdb_popularity},
        )
        json_response = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(json_response["count"], 1)
        self.assertEqual(json_response["results"][0]["id"], self.movie.id)

    def test__list__filter_wins_min(self):
        baker.make(Movie, wins=self.movie.wins - 1)

        response = self.client.get(
            self.movie_list_url,
            data={"wins_min": self.movie.wins},
        )
        json_response = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(json_response["count"], 1)
        self.assertEqual(json_response["results"][0]["id"], self.movie.id)

    def test__list__filter_wins_max(self):
        baker.make(Movie, wins=self.movie.wins + 1)

        response = self.client.get(
            self.movie_list_url,
            data={"wins_max": self.movie.wins},
        )
        json_response = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(json_response["count"], 1)
        self.assertEqual(json_response["results"][0]["id"], self.movie.id)

    def test__list__filter_nominations_min(self):
        baker.make(Movie, nominations=self.movie.nominations - 1)

        response = self.client.get(
            self.movie_list_url,
            data={"nominations_min": self.movie.nominations},
        )
        json_response = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(json_response["count"], 1)
        self.assertEqual(json_response["results"][0]["id"], self.movie.id)

    def test__list__filter_nominations_max(self):
        baker.make(Movie, nominations=self.movie.nominations + 1)

        response = self.client.get(
            self.movie_list_url,
            data={"nominations_max": self.movie.nominations},
        )
        json_response = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(json_response["count"], 1)
        self.assertEqual(json_response["results"][0]["id"], self.movie.id)

    def test__list__filter_director_full_name(self):
        baker.make(Movie)

        response = self.client.get(
            self.movie_list_url, data={"director_full_name": "Peter Jacks"}
        )
        json_response = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(json_response["count"], 1)
        self.assertEqual(json_response["results"][0]["id"], self.movie.id)

    def test__list__filter_genres(self):
        genre = baker.make(Genre)
        second_movie = baker.make(Movie)
        second_movie.genres.add(genre)

        response = self.client.get(
            self.movie_list_url,
            data={
                "genres": ",".join(
                    [
                        str(genre_id)
                        for genre_id in self.movie.genres.values_list("id", flat=True)
                    ]
                )
            },
        )
        json_response = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(json_response["count"], 1)
        self.assertEqual(json_response["results"][0]["id"], self.movie.id)

    def test__list__filter_country(self):
        country = baker.make(Country)
        second_movie = baker.make(Movie)
        second_movie.country.add(country)

        response = self.client.get(
            self.movie_list_url,
            data={
                "country": ",".join(
                    [
                        str(country_id)
                        for country_id in self.movie.country.values_list("id", flat=True)
                    ]
                )
            },
        )
        json_response = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(json_response["count"], 1)
        self.assertEqual(json_response["results"][0]["id"], self.movie.id)

    def test__list__filter_language(self):
        language = baker.make(Language)
        second_movie = baker.make(Movie)
        second_movie.language.add(language)

        response = self.client.get(
            self.movie_list_url,
            data={
                "language": ",".join(
                    [
                        str(language_id)
                        for language_id in self.movie.language.values_list(
                            "id", flat=True
                        )
                    ]
                )
            },
        )
        json_response = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(json_response["count"], 1)
        self.assertEqual(json_response["results"][0]["id"], self.movie.id)
