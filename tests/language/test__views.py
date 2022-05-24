from django.urls import reverse

from tests.base import BaseTestCase


class LanguageViewSetTestCase(BaseTestCase):
    country_list_url = reverse("language-list")

    def setUp(self) -> None:
        super(LanguageViewSetTestCase, self).setUp()
        self.create_models()

    def test__list(self):
        response = self.client.get(self.country_list_url)
        json_response = response.json()

        self.assertEqual(200, response.status_code)
        self.assertEqual(10, json_response["count"])

    def test__list__search(self):
        response = self.client.get(self.country_list_url, data={"search": "test_1"})
        json_response = response.json()

        self.assertEqual(200, response.status_code)
        self.assertEqual(1, json_response["count"])
