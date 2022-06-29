from tests.base import BaseTestCase
from TvFY.director.models import Director


class DirectorManagerTestCase(BaseTestCase):
    def test__create(self):
        director_data = {
            "first_name": "test_first_name",
            "last_name": "test_last_name",
        }

        director = Director.objects.create(**director_data)

        self.assertEqual("test_first_name test_last_name", director.full_name)
        self.assertTrue(director.tvfy_code.startswith("dt-"))
