from rest_framework.reverse import reverse

from tests.base import BaseTestCase


class GenreViewSetTestCase(BaseTestCase):
    genre_list_url = reverse("genre-list")

    def setUp(self) -> None:
        super(GenreViewSetTestCase, self).setUp()
        self.create_models()

    def test__list(self):
        expected_attrs = {
            "name",
            "detail",
        }

        response = self.client.get(self.genre_list_url)
        json_response = response.json()

        self.assertEqual(200, response.status_code)
        self.assertEqual(10, json_response["count"])
        self.assertTrue(self.is_subset(attrs=expected_attrs, results=json_response["results"]))

    def test__list__search(self):
        response = self.client.get(self.genre_list_url, data={"search": "_1"})
        json_response = response.json()

        self.assertEqual(200, response.status_code)
        self.assertEqual(1, json_response["count"])
