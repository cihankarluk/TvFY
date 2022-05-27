from django.urls import reverse

from tests.base import BaseTestCase


class SearchViewSetTestCase(BaseTestCase):
    search_url = reverse("search-list")

    def test__create__series(self):
        expected_attrs = {
            "tvfy_code",
            "name",
            "creator",
            "run_time",
            "storyline",
            "release_date",
            "is_active",
            "end_date",
            "tv_network",
            "wins",
            "nominations",
            "season_count",
            "imdb_rate",
            "imdb_vote_count",
            "imdb_popularity",
            "tv_com_rate",
            "rt_tomatometer",
            "rt_audience_rate",
            "tvfy_rate",
            "tvfy_popularity",
            "imdb_url",
            "imdb_creator_url",
            "tv_network_url",
            "rotten_tomatoes_url",
        }

        response = self.client.post(
            path=self.search_url,
            data={"name": "The Boys", "type": "series"},
        )
        json_response = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertTrue(self.is_subset(attrs=expected_attrs, results=[json_response]))

    def test__create__movie(self):
        expected_attrs = {
            "imdb_rate",
            "usa_opening_weekend",
            "imdb_vote_count",
            "director",
            "release_date",
            "ww_gross",
            "nominations",
            "id",
            "imdb_popularity",
            "language",
            "rt_tomatometer_rate",
            "wins",
            "genres",
            "usa_opening_weekend_currency",
            "rt_audience_rate",
            "rotten_tomatoes_url",
            "tvfy_code",
            "title",
            "run_time",
            "imdb_url",
            "country",
            "budget_currency",
            "budget",
            "storyline",
        }

        response = self.client.post(
            path=self.search_url,
            data={"name": "mad max fury road", "type": "movie"},
        )
        json_response = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertTrue(self.is_subset(attrs=expected_attrs, results=[json_response]))
