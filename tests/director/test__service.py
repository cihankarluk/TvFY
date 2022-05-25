from TvFY.director.models import Director
from TvFY.director.service import DirectorService
from tests.base import BaseTestCase


class DirectorServiceTestCase(BaseTestCase):

    def test__create_director(self):
        director_data = {
            "first_name": "test",
            "last_name": "test",
            "imdb_director_url": "https://www.test.com/name/test/",
        }

        director = DirectorService.create_director(director_data=director_data)

        self.assertEqual(Director.objects.get(imdb_url=director_data["imdb_director_url"]), director)

    def test__update_director(self):
        director_data = {
            "first_name": "test",
            "last_name": "test",
            "imdb_url": "https://www.test.com/name/0/",
            "rt_url": "https://www.rt-test.com/name/0/",
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
        director = self.create_director(count=1)[0]

        DirectorService.update_director(director_data=director_data, director_obj=director)

        director.refresh_from_db()
        for key, value in director_data.items():
            self.assertEqual(getattr(director, key), value)
