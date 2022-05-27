from TvFY.country.models import Country
from TvFY.country.service import CountryService
from tests.base import BaseTestCase


class CountryServiceTestCase(BaseTestCase):

    def test__get_or_create_language(self):
        country_object = CountryService.get_or_create_country(country_name="Turkey")

        self.assertTrue(isinstance(country_object, Country))
        self.assertEqual("Turkey", country_object.name)

    def test__get_or_create_multiple_country(self):
        search_data = {"country": ["Holland", "Canada", "Germany"]}

        objects = CountryService.get_or_create_multiple_country(search_data=search_data)

        self.assertEqual(3, len(objects))

    def test__get_or_create_multiple_country__empty_search_data(self):
        search_data = {}

        objects = CountryService.get_or_create_multiple_country(search_data=search_data)

        self.assertEqual(0, len(objects))
