from django.test import TestCase
from model_bakery import baker
from rest_framework.reverse import reverse
from rest_framework.test import APIClient


class ActorViewTestCase(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.url = reverse("actor")

    def test_get_actor_with_correct_request(self):
        baker.make(
            "actor.Actor",
            first_name="Keanu",
            last_name="Reeves",
            imdb_url="test_url",
            perks=["actor", "producer", "soundtrack"],
        )

        response = self.client.get(self.url, content_type="application/json")
        json_response = response.json()
        result = json_response["results"][0]

        self.assertEqual(response.status_code, 200)
        self.assertTrue(result["first_name"], "Keanu")
        self.assertEqual(result["perks"], ["actor", "producer", "soundtrack"])
