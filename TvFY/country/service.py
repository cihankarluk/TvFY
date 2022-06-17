from typing import List, Any

from TvFY.country.models import Country


class CountryService:

    @classmethod
    def get_or_create_country(cls, country_name: str) -> Country:
        country_object, _ = Country.objects.get_or_create(name=country_name)
        return country_object

    @classmethod
    def get_or_create_multiple_country(cls, search_data: dict[str, Any]) -> List[Country]:
        country_objects = []
        for country in search_data.get("country", []):
            country_objects.append(cls.get_or_create_country(country_name=country))
        return country_objects
