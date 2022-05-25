from TvFY.country.models import Country


class CountryService:

    @classmethod
    def get_or_create_country(cls, country_name: str) -> Country:
        country_object, _ = Country.objects.get_or_create(name=country_name)
        return country_object
