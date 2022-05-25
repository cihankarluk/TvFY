from TvFY.actor.models import Actor
from tests.base import BaseTestCase


class ActorManagerTestCase(BaseTestCase):

    def test__create(self):
        actor_data = {
            "first_name": "test_first_name",
            "last_name": "test_last_name",
        }

        actor = Actor.objects.create(**actor_data)

        self.assertEqual("test_first_name test_last_name", actor.full_name)
        self.assertTrue(actor.tvfy_code.startswith("ac-"))
