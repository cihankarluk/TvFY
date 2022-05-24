from rest_framework.reverse import reverse

from TvFY.country.models import Country
from tests.base import BaseTestCase


class ActorViewSetTestCase(BaseTestCase):
    actor_list_url = reverse("actor-list")

    def setUp(self) -> None:
        super(ActorViewSetTestCase, self).setUp()
        self.create_models()

    def test__list(self):
        born_at = Country.objects.first()
        died_at = Country.objects.last()
        self.create_actor(index_start=11, count=1, born_at=born_at, died_at=died_at, born_date=self.now,
                          died_date=self.now)

        response = self.client.get(self.actor_list_url)
        json_response = response.json()

        self.assertEqual(200, response.status_code)
        self.assertEqual(11, json_response["count"])

    def test__list__search(self):
        response = self.client.get(self.actor_list_url, data={"search": "_1"})
        json_response = response.json()

        self.assertEqual(200, response.status_code)
        self.assertEqual(1, json_response["count"])
