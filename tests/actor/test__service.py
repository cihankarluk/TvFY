from TvFY.actor.models import Actor
from TvFY.actor.service import ActorService
from tests.base import BaseTestCase


class ActorServiceTestCase(BaseTestCase):

    def test__create_actor(self):
        actor_data = {
            "first_name": "test",
            "last_name": "test",
            "imdb_actor_url": "https://www.test.com/name/test/",
        }

        actor = ActorService.create_actor(actor_data=actor_data)

        self.assertEqual(Actor.objects.get(imdb_url=actor_data["imdb_actor_url"]), actor)

    def test__create_multiple_actor(self):
        cast_data = [{
            "first_name": "test",
            "last_name": "test",
            "imdb_actor_url": "https://www.test.com/name/0/",
        }, {
            "first_name": "test_2",
            "last_name": "test_2",
            "imdb_actor_url": "https://www.test.com/name/2/"
        }]
        actor = self.create_actor(count=1)[0]

        return_value = ActorService.create_multiple_actor(cast_data=cast_data)

        self.assertEqual(Actor.objects.count(), 2)
        self.assertEqual(return_value["https://www.test.com/name/0/"]["actor"], actor)
        second_actor = Actor.objects.get(imdb_url="https://www.test.com/name/2/")
        self.assertEqual(return_value["https://www.test.com/name/2/"]["actor"], second_actor)

    def test__create_multiple_actor__empty_cast_data(self):
        cast_data = []

        ActorService.create_multiple_actor(cast_data=cast_data)

        self.assertEqual(Actor.objects.count(), 0)

    def test__update_actor(self):
        actor_data = {
            "first_name": "test",
            "last_name": "test",
            "imdb_url": "https://www.test.com/name/0/",
            "born_date": self.now,
            "born_at": "Jamaica",
            "died_date": self.now,
            "died_at": "Holland",
            "perks": ["Actor", "High"],
            "oscars": 4,
            "oscar_nominations": 20,
            "wins": 420,
            "nominations": 10,
            "is_updated": True
        }
        actor = self.create_actor(count=1)[0]

        ActorService.update_actor(actor_data=actor_data, actor=actor)

        actor.refresh_from_db()
        for key, value in actor_data.items():
            self.assertEqual(getattr(actor, key), value)
