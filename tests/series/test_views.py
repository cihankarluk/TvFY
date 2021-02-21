from model_bakery import baker
from rest_framework.reverse import reverse

from tests.base.test_base import BaseView
from TvFY.core.helpers import read_file


class SeriesViewTestCase(BaseView):
    def setUp(self) -> None:
        super(SeriesViewTestCase, self).setUp()
        self.series_url = reverse("series")
        self.series_detail_url = reverse(
            "series_detail", kwargs={"tvfy_code": "test_tvfy_code"}
        )
        json_file = read_file("tests/data/series_data.json", is_json=True)
        baker.make("series.Series", **json_file)

    def test_get_series_with_correct_request(self):
        response = self.client.get(self.series_url, **self.headers)
        self.assertEqual(response.status_code, 200)

        json_response = response.json()
        result = json_response["results"][0]
        self.assertTrue(result["tvfy_code"])
        self.assertTrue(result["name"])
        self.assertTrue(result["release_date"])
        self.assertTrue(result["is_active"])
        self.assertTrue(result["tv_network"])
        self.assertTrue(result["imdb_rate"])
        self.assertTrue(result["rt_tomatometer"])
        self.assertTrue(result["rt_audience_rate"])

    def test_get_series_detail_with_correct_request(self):
        response = self.client.get(self.series_detail_url, **self.headers)
        self.assertEqual(response.status_code, 200)

        result = response.json()
        self.assertTrue(result["tvfy_code"])
        self.assertTrue(result["name"])
        self.assertTrue(result["creator"])
        self.assertTrue(result["run_time"])
        self.assertTrue(result["storyline"])
        self.assertTrue(result["release_date"])
        self.assertTrue(result["is_active"])
        self.assertIsNone(result["end_date"])
        self.assertTrue(result["tv_network"])
        self.assertTrue(result["wins"])
        self.assertTrue(result["nominations"])
        self.assertTrue(result["season_count"])
        self.assertTrue(result["imdb_rate"])
        self.assertTrue(result["imdb_vote_count"])
        self.assertTrue(result["imdb_popularity"])
        self.assertIsNone(result["tv_com_rate"])
        self.assertTrue(result["rt_tomatometer"])
        self.assertTrue(result["rt_audience_rate"])
        self.assertIsNone(result["tvfy_rate"])
        self.assertIsNone(result["tvfy_popularity"])
        self.assertTrue(result["imdb_url"])
        self.assertTrue(result["imdb_creator_url"])
        self.assertIsNone(result["tv_network_url"])
        self.assertTrue(result["rotten_tomatoes_url"])

    def test_get_series_detail_with_wrong_code(self):
        url = f"{self.series_detail_url}a"
        response = self.client.get(url, **self.headers)
        self.assertEqual(response.status_code, 404)

        expected_result = {
            "status_code": 404,
            "code": "SERIES_DOES_NOT_EXIST",
            "error_message": {"detail": "Series does not exists."},
        }
        result = response.json()
        self.assertEqual(result, expected_result)
