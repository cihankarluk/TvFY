from rest_framework.reverse import reverse

from TvFY.country.models import Country
from tests.base import BaseTestCase


class ActorViewSetTestCase(BaseTestCase):
    actor_list_url = reverse("actor-list")

    @classmethod
    def get_actor_detail_url(cls, tvfy_code):
        return reverse("actor-detail", kwargs={'tvfy_code': tvfy_code})

    def setUp(self) -> None:
        super(ActorViewSetTestCase, self).setUp()
        self.actor = self.create_actor()[0]

    def test__list(self):
        expected_attrs = {
            "tvfy_code",
            "first_name",
            "last_name",
            "full_name",
            "imdb_url",
            "born_date",
            "born_at",
            "died_date",
            "died_at",
            "perks",
            "oscars",
            "oscar_nominations",
            "wins",
            "nominations",
        }
        born_at = Country.objects.first()
        died_at = Country.objects.last()
        self.create_actor(index_start=11, count=1, born_at=born_at, died_at=died_at, born_date=self.now,
                          died_date=self.now)

        response = self.client.get(self.actor_list_url)
        json_response = response.json()

        self.assertEqual(200, response.status_code)
        self.assertEqual(11, json_response["count"])
        self.assertTrue(self.is_subset(attrs=expected_attrs, results=json_response["results"]))

    def test__list__search(self):
        response = self.client.get(self.actor_list_url, data={"search": "_1"})
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
            "born_date",
            "born_at",
            "died_date",
            "died_at",
            "perks",
            "oscars",
            "oscar_nominations",
            "wins",
            "nominations",
            "movie_cast",
            "series_cast",
        }

        response = self.client.get(
            self.get_actor_detail_url(self.actor.tvfy_code),
        )
        json_response = response.json()

        self.assertEqual(200, response.status_code)
        self.assertTrue(self.is_subset(attrs=expected_attrs, results=json_response))

    def test__retrieve__not_exists(self):
        expected_response = {
            'code': 404,
            'type': 'ActorNotFoundError',
            'reason': 'Actor with notExists code does not exists.'
        }

        response = self.client.get(
            self.get_actor_detail_url("notExists"),
        )
        json_response = response.json()

        self.assertEqual(404, response.status_code)
        self.assertEqual(expected_response, json_response)
