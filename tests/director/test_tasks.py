from django.test import TestCase
from model_bakery import baker

from TvFY.director.models import Director
from TvFY.director.tasks import fill_director_data


class TasksTestCase(TestCase):
    def setUp(self) -> None:
        pass

    def test_fill_director_data_if_imdb_url_does_not_exists(self):
        director = baker.make("director.Director", imdb_url=None, born=None)
        fill_director_data()

        director = Director.objects.get(id=director.id)
        self.assertIsNone(director.born)

    def test_fill_director_data_with_correct_url(self):
        # Christopher Nolan
        director = baker.make(
            "director.Director", imdb_url="https://www.imdb.com/name/nm0634240/"
        )
        fill_director_data()

        director = Director.objects.get(id=director.id)

        self.assertTrue(director.born)
        self.assertTrue(director.born_at)
        self.assertIsNone(director.died)
        self.assertTrue(director.perks)
        self.assertTrue(director.oscar_nominations)
        self.assertTrue(director.wins)
        self.assertTrue(director.nominations)
