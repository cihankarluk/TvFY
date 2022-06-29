from rest_framework.reverse import reverse

from tests.base import BaseTestCase
from TvFY.country.models import Country


class DirectorViewSetTestCase(BaseTestCase):
    director_list_url = reverse("director-list")

    @classmethod
    def get_director_detail_url(cls, tvfy_code):
        return reverse("director-detail", kwargs={"tvfy_code": tvfy_code})

    def setUp(self) -> None:
        super().setUp()
        self.director = self.create_director()[0]

    def test__list(self):
        expected_attrs = {
            "tvfy_code",
            "first_name",
            "last_name",
            "full_name",
            "imdb_url",
            "rt_url",
            "born_at",
            "born_date",
            "died_at",
            "died_date",
            "perks",
            "oscars",
            "oscar_nominations",
            "wins",
            "nominations",
        }
        born_at = Country.objects.first()
        died_at = Country.objects.last()
        self.create_director(
            index_start=11,
            count=1,
            born_at=born_at,
            died_at=died_at,
            born_date=self.now,
            died_date=self.now,
        )

        response = self.client.get(self.director_list_url)
        json_response = response.json()

        self.assertEqual(200, response.status_code)
        self.assertEqual(11, json_response["count"])
        self.assertTrue(self.is_subset(attrs=expected_attrs, results=json_response["results"]))

    def test__list__search(self):
        response = self.client.get(self.director_list_url, data={"search": "_1"})
        json_response = response.json()

        self.assertEqual(200, response.status_code)
        self.assertEqual(1, json_response["count"])

    def test__retrieve(self):
        expected_attrs = {
            "tvfy_code",
            "first_name",
            "last_name",
            "full_name",
            "imdb_url",
            "rt_url",
            "born_at",
            "born_date",
            "died_at",
            "died_date",
            "perks",
            "oscars",
            "oscar_nominations",
            "wins",
            "nominations",
            "director_movie",
            "director_series",
        }

        response = self.client.get(
            self.get_director_detail_url(self.director.tvfy_code),
        )
        json_response = response.json()

        self.assertEqual(200, response.status_code)
        self.assertTrue(self.is_subset(attrs=expected_attrs, results=json_response))

    def test__retrieve__not_exists(self):
        expected_response = {
            "code": 404,
            "type": "DirectorNotFoundError",
            "reason": "Director with notExists code does not exists.",
        }

        response = self.client.get(
            self.get_director_detail_url("notExists"),
        )
        json_response = response.json()

        self.assertEqual(404, response.status_code)
        self.assertEqual(expected_response, json_response)
