from model_bakery import baker
from rest_framework.reverse import reverse

from TvFY.core.helpers import read_file
from TvFY.series.service import SeriesService
from tests.base import BaseTestCase


class SeriesViewSetTestCase(BaseTestCase):
    series_list_url = reverse("series-list")

    @classmethod
    def get_series_detail_url(cls, tvfy_code):
        return reverse("series-detail", kwargs={'tvfy_code': tvfy_code})

    @classmethod
    def get_cast_url(cls, tvfy_code):
        return reverse("series-cast", kwargs={'tvfy_code': tvfy_code})

    def setUp(self) -> None:
        super(SeriesViewSetTestCase, self).setUp()
        series_data = self.read_file("series_the_boys.json", is_json=True)
        self.series = SeriesService.create_or_update_series(search_data=series_data)

    def test__retrieve(self):
        expected_attrs = {
            "tvfy_code",
            "title",
            "storyline",
            "release_date",
            "end_date",
            "run_time",
            "is_active",
            "season_count",
            "wins",
            "nominations",
            "tv_network",
            "imdb_rate",
            "imdb_vote_count",
            "imdb_popularity",
            "imdb_url",
            "rt_tomatometer_rate",
            "rt_audience_rate",
            "rotten_tomatoes_url",
            "tv_com_rate",
            "tv_com_url",
            "creator",
            "genres",
            "country",
            "language",
            "cast",
        }

        response = self.client.get(self.get_series_detail_url(self.series.tvfy_code))
        json_response = response.json()

        self.assertEqual(200, response.status_code)
        self.assertTrue(self.is_subset(attrs=expected_attrs, results=json_response))
