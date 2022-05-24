from TvFY.language.models import Language


class LanguageService:

    @classmethod
    def get_or_create_language(cls, language_name: str):
        language_object, _ = Language.objects.get_or_create(name=language_name)
        return language_object
