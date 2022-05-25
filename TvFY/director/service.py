from TvFY.country.service import CountryService
from TvFY.director.models import Director


class DirectorService:

    @classmethod
    def create_director(cls, director_data: dict) -> Director:
        director = Director.objects.create(
            first_name=director_data["first_name"],
            last_name=director_data["last_name"],
            imdb_url=director_data["imdb_director_url"],
        )
        return director

    @classmethod
    def update_director(cls, director_data: dict, director_obj: Director):
        born_at = director_data.pop("born_at", None)
        died_at = director_data.pop("died_at", None)
        for field, value in director_data.items():
            setattr(director_obj, field, value)
        director_obj.born_at = CountryService.get_or_create_country(country_name=born_at)
        director_obj.died_at = CountryService.get_or_create_country(country_name=died_at)
        director_obj.save()
