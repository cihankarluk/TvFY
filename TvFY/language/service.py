from typing import Any, List

from TvFY.language.models import Language


class LanguageService:
    @classmethod
    def get_or_create_language(cls, language_name: str) -> Language:
        language_object, _ = Language.objects.get_or_create(name=language_name)
        return language_object

    @classmethod
    def get_or_create_multiple_language(cls, search_data: dict[str, Any]) -> List[Language]:
        language_objects = []
        for language in search_data.get("language", []):
            language_objects.append(cls.get_or_create_language(language_name=language))
        return language_objects
