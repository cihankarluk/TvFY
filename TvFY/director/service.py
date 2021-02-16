from TvFY.core.models import Country
from TvFY.director.models import Director


class DirectorService:
    def __init__(self, search_data: dict, director_obj: Director):
        self.search_data = search_data
        self.director = director_obj

    @staticmethod
    def get_or_create_country(country):
        if country:
            country, _ = Country.objects.get_or_create(country=country)
        return country

    def update_director(self):
        born_at = self.search_data.pop("born_at", None)
        died_at = self.search_data.pop("died_at", None)
        for field, value in self.search_data.items():
            setattr(self.director, field, value)
        self.director.born_at = self.get_or_create_country(country=born_at)
        self.director.died_at = self.get_or_create_country(country=died_at)
        self.director.save()
