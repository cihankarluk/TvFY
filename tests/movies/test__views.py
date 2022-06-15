from datetime import timedelta

from django.urls import reverse
from model_bakery import baker

from TvFY.country.models import Country
from TvFY.genre.models import Genre
from TvFY.language.models import Language
from TvFY.movies.models import Movie
from TvFY.movies.service import MovieService
from tests.base import BaseTestCase


class MovieViewSetTestCase(BaseTestCase):
    movie_list_url = reverse("movie-list")

    @classmethod
    def get_movie_detail_url(cls, tvfy_code):
        return reverse("movie-detail", kwargs={'tvfy_code': tvfy_code})

    @classmethod
    def get_cast_url(cls, tvfy_code):
        return reverse("movie-cast", kwargs={'tvfy_code': tvfy_code})

    def setUp(self) -> None:
        super(MovieViewSetTestCase, self).setUp()
        movie_data = self.read_file("movie_batman.json", is_json=True)
        self.movie = MovieService.create_or_update_movie(search_data=movie_data)

    def test__list(self):
        expected_attrs = {
            "tvfy_code",
            "title",
            "storyline",
            "release_date",
            "wins",
            "nominations",
            "oscar_wins",
            "oscar_nominations",
            "run_time",
            "imdb_rate",
            "imdb_vote_count",
            "imdb_popularity",
            "imdb_url",
            "rt_tomatometer_rate",
            "rt_tomatometer_count",
            "rt_audience_rate",
            "rt_audience_count",
            "rotten_tomatoes_url",
            "budget_amount",
            "budget_currency",
            "usa_ow_amount",
            "usa_ow_currency",
            "ww_amount",
            "ww_currency",
            "metacritic_score",
            "director",
            "genres",
            "country",
            "language",
        }

        response = self.client.get(self.movie_list_url)
        json_response = response.json()

        self.assertEqual(response.status_code, 200)
        self.is_subset(attrs=expected_attrs, results=json_response["results"])

    def test__list__filter_release_date_after(self):
        movie1 = baker.make(Movie, release_date=self.now)
        baker.make(Movie, release_date=self.now - timedelta(days=2))

        response = self.client.get(
            self.movie_list_url,
            data={"release_date_after": (self.now - timedelta(days=1)).strftime("%Y-%m-%d")},
        )
        json_response = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(json_response["count"], 1)
        self.assertEqual(json_response["results"][0]["tvfy_code"], movie1.tvfy_code)

    def test__list__filter_release_date_before(self):
        baker.make(Movie, release_date=self.now)
        movie2 = baker.make(Movie, release_date=self.now - timedelta(days=2))

        response = self.client.get(
            self.movie_list_url,
            data={"release_date_before": (self.now - timedelta(days=1)).strftime("%Y-%m-%d")},
        )
        json_response = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(json_response["count"], 1)
        self.assertEqual(json_response["results"][0]["tvfy_code"], movie2.tvfy_code)

    def test__list__filter_run_time_min(self):
        baker.make(Movie, run_time=self.movie.run_time - 1)

        response = self.client.get(
            self.movie_list_url,
            data={"run_time_min": self.movie.run_time},
        )
        json_response = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(json_response["count"], 1)
        self.assertEqual(json_response["results"][0]["tvfy_code"], self.movie.tvfy_code)

    def test__list__filter_run_time_max(self):
        baker.make(Movie, run_time=self.movie.run_time + 1)

        response = self.client.get(
            self.movie_list_url,
            data={"run_time_max": self.movie.run_time},
        )
        json_response = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(json_response["count"], 1)
        self.assertEqual(json_response["results"][0]["tvfy_code"], self.movie.tvfy_code)

    def test__list__filter_rt_tomatometer_rate_min(self):
        baker.make(Movie, rt_tomatometer_rate=self.movie.rt_tomatometer_rate - 1)

        response = self.client.get(
            self.movie_list_url,
            data={"rt_tomatometer_rate_min": self.movie.rt_tomatometer_rate},
        )
        json_response = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(json_response["count"], 1)
        self.assertEqual(json_response["results"][0]["tvfy_code"], self.movie.tvfy_code)

    def test__list__filter_rt_tomatometer_rate_max(self):
        baker.make(Movie, rt_tomatometer_rate=self.movie.rt_tomatometer_rate + 1)

        response = self.client.get(
            self.movie_list_url,
            data={"rt_tomatometer_rate_max": self.movie.rt_tomatometer_rate},
        )
        json_response = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(json_response["count"], 1)
        self.assertEqual(json_response["results"][0]["tvfy_code"], self.movie.tvfy_code)

    def test__list__filter_rt_audience_rate_min(self):
        baker.make(Movie, rt_audience_rate=self.movie.rt_audience_rate - 1)

        response = self.client.get(
            self.movie_list_url,
            data={"rt_audience_rate_min": self.movie.rt_audience_rate},
        )
        json_response = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(json_response["count"], 1)
        self.assertEqual(json_response["results"][0]["tvfy_code"], self.movie.tvfy_code)

    def test__list__filter_rt_audience_rate_max(self):
        baker.make(Movie, rt_audience_rate=self.movie.rt_audience_rate + 1)

        response = self.client.get(
            self.movie_list_url,
            data={"rt_audience_rate_max": self.movie.rt_audience_rate},
        )
        json_response = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(json_response["count"], 1)
        self.assertEqual(json_response["results"][0]["tvfy_code"], self.movie.tvfy_code)

    def test__list__filter_imdb_rate_min(self):
        baker.make(Movie, imdb_rate=self.movie.imdb_rate - 0.1)

        response = self.client.get(
            self.movie_list_url,
            data={"imdb_rate_min": self.movie.imdb_rate},
        )
        json_response = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(json_response["count"], 1)
        self.assertEqual(json_response["results"][0]["tvfy_code"], self.movie.tvfy_code)

    def test__list__filter_imdb_rate_max(self):
        baker.make(Movie, imdb_rate=self.movie.imdb_rate + 0.1)

        response = self.client.get(
            self.movie_list_url,
            data={"imdb_rate_max": self.movie.imdb_rate},
        )
        json_response = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(json_response["count"], 1)
        self.assertEqual(json_response["results"][0]["tvfy_code"], self.movie.tvfy_code)

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
        self.assertEqual(json_response["results"][0]["tvfy_code"], self.movie.tvfy_code)

    def test__list__filter_imdb_popularity_min(self):
        baker.make(Movie, imdb_popularity=self.movie.imdb_popularity - 1)

        response = self.client.get(
            self.movie_list_url,
            data={"imdb_popularity_min": self.movie.imdb_popularity},
        )
        json_response = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(json_response["count"], 1)
        self.assertEqual(json_response["results"][0]["tvfy_code"], self.movie.tvfy_code)

    def test__list__filter_imdb_popularity_max(self):
        baker.make(Movie, imdb_popularity=self.movie.imdb_popularity + 1)

        response = self.client.get(
            self.movie_list_url,
            data={"imdb_popularity_max": self.movie.imdb_popularity},
        )
        json_response = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(json_response["count"], 1)
        self.assertEqual(json_response["results"][0]["tvfy_code"], self.movie.tvfy_code)

    def test__list__filter_wins_min(self):
        baker.make(Movie, wins=self.movie.wins - 1)

        response = self.client.get(
            self.movie_list_url,
            data={"wins_min": self.movie.wins},
        )
        json_response = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(json_response["count"], 1)
        self.assertEqual(json_response["results"][0]["tvfy_code"], self.movie.tvfy_code)

    def test__list__filter_wins_max(self):
        baker.make(Movie, wins=self.movie.wins + 1)

        response = self.client.get(
            self.movie_list_url,
            data={"wins_max": self.movie.wins},
        )
        json_response = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(json_response["count"], 1)
        self.assertEqual(json_response["results"][0]["tvfy_code"], self.movie.tvfy_code)

    def test__list__filter_nominations_min(self):
        baker.make(Movie, nominations=self.movie.nominations - 1)

        response = self.client.get(
            self.movie_list_url,
            data={"nominations_min": self.movie.nominations},
        )
        json_response = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(json_response["count"], 1)
        self.assertEqual(json_response["results"][0]["tvfy_code"], self.movie.tvfy_code)

    def test__list__filter_nominations_max(self):
        baker.make(Movie, nominations=self.movie.nominations + 1)

        response = self.client.get(
            self.movie_list_url,
            data={"nominations_max": self.movie.nominations},
        )
        json_response = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(json_response["count"], 1)
        self.assertEqual(json_response["results"][0]["tvfy_code"], self.movie.tvfy_code)

    def test__list__filter_director_full_name(self):
        baker.make(Movie)

        response = self.client.get(self.movie_list_url, data={"director_full_name": self.movie.director.full_name})
        json_response = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(json_response["count"], 1)
        self.assertEqual(json_response["results"][0]["tvfy_code"], self.movie.tvfy_code)

    def test__list__filter_genres(self):
        genre = baker.make(Genre)
        movie2 = baker.make(Movie)
        movie2.genres.add(genre)

        response = self.client.get(
            self.movie_list_url,
            data={"genres": ",".join([str(genre_id) for genre_id in self.movie.genres.values_list("id", flat=True)])},
        )
        json_response = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(json_response["count"], 1)
        self.assertEqual(json_response["results"][0]["tvfy_code"], self.movie.tvfy_code)

    def test__list__filter_country(self):
        country = baker.make(Country)
        movie2 = baker.make(Movie)
        movie2.country.add(country)

        response = self.client.get(
            self.movie_list_url,
            data={
                "country": ",".join([str(country_id) for country_id in self.movie.country.values_list("id", flat=True)])
            },
        )
        json_response = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(json_response["count"], 1)
        self.assertEqual(json_response["results"][0]["tvfy_code"], self.movie.tvfy_code)

    def test__list__filter_language(self):
        language = baker.make(Language)
        movie2 = baker.make(Movie)
        movie2.language.add(language)

        response = self.client.get(
            self.movie_list_url,
            data={
                "language": ",".join(
                    [str(language_id) for language_id in self.movie.language.values_list("id", flat=True)]
                )
            },
        )
        json_response = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(json_response["count"], 1)
        self.assertEqual(json_response["results"][0]["tvfy_code"], self.movie.tvfy_code)

    def test__search__title(self):
        movie2 = baker.make(Movie, title="Mahmut Tuncer Welcome to my Halay")

        response = self.client.get(
            self.movie_list_url,
            data={"search": "Mahmut Tuncer"}
        )
        json_response = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(json_response["count"], 1)
        self.assertEqual(json_response["results"][0]["tvfy_code"], movie2.tvfy_code)

    def test__search__tvfy_code(self):
        movie2 = baker.make(Movie)

        response = self.client.get(
            self.movie_list_url,
            data={"search": movie2.tvfy_code}
        )
        json_response = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(json_response["count"], 1)
        self.assertEqual(json_response["results"][0]["tvfy_code"], movie2.tvfy_code)

    def test__search__tvfy_code__not_exact_code(self):
        movie2 = baker.make(Movie)

        response = self.client.get(
            self.movie_list_url,
            data={"search": movie2.tvfy_code[:5]}
        )
        json_response = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(json_response["count"], 0)

    def test__ordering_fields_imdb_rate(self):
        movie1 = baker.make(Movie, imdb_rate=self.movie.imdb_rate - 1)
        movie2 = baker.make(Movie, imdb_rate=self.movie.imdb_rate - 2)

        response = self.client.get(
            self.movie_list_url,
            data={"ordering": "-imdb_rate"}
        )
        json_response = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(json_response["count"], 3)
        self.assertEqual(json_response["results"][0]["tvfy_code"], self.movie.tvfy_code)
        self.assertEqual(json_response["results"][1]["tvfy_code"], movie1.tvfy_code)
        self.assertEqual(json_response["results"][2]["tvfy_code"], movie2.tvfy_code)

    def test__retrieve(self):
        expected_attrs = {
            "tvfy_code",
            "title",
            "storyline",
            "release_date",
            "wins",
            "nominations",
            "oscar_wins",
            "oscar_nominations",
            "run_time",
            "imdb_rate",
            "imdb_vote_count",
            "imdb_popularity",
            "imdb_url",
            "rt_tomatometer_rate",
            "rt_tomatometer_count",
            "rt_audience_rate",
            "rt_audience_count",
            "rotten_tomatoes_url",
            "budget_amount",
            "budget_currency",
            "usa_ow_amount",
            "usa_ow_currency",
            "ww_amount",
            "ww_currency",
            "metacritic_score",
            "director",
            "genres",
            "country",
            "language",
            "cast",
        }

        response = self.client.get(
            self.get_movie_detail_url(self.movie.tvfy_code),
        )
        json_response = response.json()

        self.assertEqual(200, response.status_code)
        self.assertTrue(self.is_subset(attrs=expected_attrs, results=json_response))

    def test__retrieve__not_exists(self):
        expected_result = {
            'code': 404,
            'type': 'MovieNotFoundError',
            'reason': 'Movie with notExists code does not exists.'
        }
        response = self.client.get(
            self.get_movie_detail_url("notExists"),
        )
        json_response = response.json()

        self.assertEqual(404, response.status_code)
        self.assertEqual(expected_result, json_response)

    def test__get_cast(self):
        expected_attrs = {
            "character_name",
            "actor"
        }
        response = self.client.get(
            self.get_cast_url(self.movie.tvfy_code),
        )
        json_response = response.json()

        self.assertEqual(200, response.status_code)
        self.assertTrue(self.is_subset(attrs=expected_attrs, results=json_response))

    def test__cast__not_exists(self):
        expected_result = {
            'code': 404,
            'type': 'MovieNotFoundError',
            'reason': 'Movie with notExists code does not exists.'
        }
        response = self.client.get(
            self.get_movie_detail_url("notExists"),
        )
        json_response = response.json()

        self.assertEqual(404, response.status_code)
        self.assertEqual(expected_result, json_response)
