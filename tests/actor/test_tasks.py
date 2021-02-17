from django.test import TestCase
from model_bakery import baker

from TvFY.actor.models import Actor
from TvFY.actor.tasks import fill_actor_data


class TasksTestCase(TestCase):
    def test_fill_director_data_if_imdb_url_does_not_exists(self):
        actor = baker.make("actor.Actor", imdb_url=None, born=None)
        fill_actor_data()

        actor = Actor.objects.get(id=actor.id)
        self.assertIsNone(actor.born)

    def test_fill_director_data_with_correct_url(self):
        # Keanu Reeves
        actor = baker.make("actor.Actor", imdb_url="https://www.imdb.com/name/nm0000206/")
        fill_actor_data()

        actor = Actor.objects.get(id=actor.id)

        self.assertTrue(actor.born)
        self.assertTrue(actor.born_at)
        self.assertIsNone(actor.died)
        self.assertTrue(actor.perks)
        self.assertTrue(actor.wins)
        self.assertTrue(actor.nominations)
