from TvFY.language.models import Language
from TvFY.language.service import LanguageService
from tests.base import BaseTestCase


class LanguageServiceTestCase(BaseTestCase):

    def test__get_or_create_language(self):
        language_object = LanguageService.get_or_create_language(language_name="Turkish")

        self.assertTrue(isinstance(language_object, Language))
        self.assertEqual("Turkish", language_object.name)

    def test__get_or_create_multiple_language(self):
        search_data = {"language": ["Mandarin", "Turkish", "Danish"]}

        objects = LanguageService.get_or_create_multiple_language(search_data=search_data)

        self.assertEqual(3, len(objects))

    def test__get_or_create_multiple_language__empty_search_data(self):
        search_data = {}

        objects = LanguageService.get_or_create_multiple_language(search_data=search_data)

        self.assertEqual(0, len(objects))
