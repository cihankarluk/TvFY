from tests.base import BaseTestCase
from TvFY.core.exceptions import NotAbleToFindDirectorSourceUrl
from TvFY.director.service import DirectorService


class DirectorServiceTestCase(BaseTestCase):
    def test__check_source_urls(self):
        """Expect to not raise any errors."""
        search_data = {"imdb_director_url": "test"}
        result = DirectorService.check_source_urls(search_data=search_data)
        self.assertIsNone(result)

        search_data = {"rt_director_url": "test"}
        result = DirectorService.check_source_urls(search_data=search_data)
        self.assertIsNone(result)

        search_data = {"imdb_director_url": "test", "rt_director_url": "test"}
        result = DirectorService.check_source_urls(search_data=search_data)
        self.assertIsNone(result)

    def test__check_source_url__raise_NotAbleToFindDirectorSourceUrl(self):  # noqa: N802
        search_data = {}
        with self.assertRaises(NotAbleToFindDirectorSourceUrl):
            DirectorService.check_source_urls(search_data=search_data)

    def test__get_director(self):
        result = DirectorService.get_director(filter_map={"imdb_url": "test"})

        self.assertIsNone(result)

    def test__get_director__exists(self):
        director = self.create_director()[0]

        result = DirectorService.get_director(filter_map={"imdb_url": director.imdb_url})

        self.assertEqual(director, result)

    def test__get_or_create_director__imdb_url(self):
        search_data = {
            "imdb_director": {
                "first_name": "imdb_first_name",
                "last_name": "imdb_last_name",
            },
            "imdb_director_url": "https://www.test.com/name/test/",
        }

        director = DirectorService.get_or_create_director(search_data=search_data)

        self.assertEqual("imdb_first_name", director.first_name)
        self.assertEqual("imdb_last_name", director.last_name)
        self.assertEqual("https://www.test.com/name/test/", director.imdb_url)
        self.assertIsNone(director.rt_url)

    def test__get_or_create_director__rt_url(self):
        search_data = {
            "rt_director": {
                "first_name": "rt_first_name",
                "last_name": "rt_last_name",
            },
            "rt_director_url": "https://www.test.com/name/test/",
        }

        director = DirectorService.get_or_create_director(search_data=search_data)

        self.assertEqual("rt_first_name", director.first_name)
        self.assertEqual("rt_last_name", director.last_name)
        self.assertEqual("https://www.test.com/name/test/", director.rt_url)
        self.assertIsNone(director.imdb_url)

    def test__get_or_create_director__imdb_url_rt_url(self):
        search_data = {
            "imdb_director": {
                "first_name": "imdb_first_name",
                "last_name": "imdb_last_name",
            },
            "imdb_director_url": "https://www.test.com/name/test/",
            "rt_director_url": "https://www.rt-test.com/name/test/",
        }

        director = DirectorService.get_or_create_director(search_data=search_data)

        self.assertEqual("imdb_first_name", director.first_name)
        self.assertEqual("imdb_last_name", director.last_name)
        self.assertEqual("https://www.test.com/name/test/", director.imdb_url)
        self.assertEqual("https://www.rt-test.com/name/test/", director.rt_url)

    def test__get_or_create_director__director_exists(self):
        director = self.create_director()[0]

        search_data = {
            "imdb_director": {
                "first_name": "imdb_first_name",
                "last_name": "imdb_last_name",
            },
            "imdb_director_url": director.imdb_url,
        }

        result = DirectorService.get_or_create_director(search_data=search_data)

        self.assertEqual(director, result)

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
            "is_updated": True,
        }
        director = self.create_director(count=1)[0]

        DirectorService.update_director(director_data=director_data, director_obj=director)

        director.refresh_from_db()
        for key, value in director_data.items():
            self.assertEqual(getattr(director, key), value)
