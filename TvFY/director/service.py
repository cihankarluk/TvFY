from typing import Optional

from TvFY.core.exceptions import NotAbleToFindDirectorSourceUrl
from TvFY.country.service import CountryService
from TvFY.director.models import Director


class DirectorService:

    @classmethod
    def check_source_urls(cls, search_data: dict) -> None:
        """
        At least one of them concur to find data about that movie.
        """
        if not (search_data.get("imdb_director_url") or search_data.get("rt_director_url")):
            raise NotAbleToFindDirectorSourceUrl(
                "Cannot find source url for that director. If you know address please contact."
            )
        return None

    @classmethod
    def get_director(cls, filter_map: dict) -> Optional[Director]:
        director_query = Director.objects.filter(**filter_map)
        if director_query.exists():
            director = director_query.get()
        else:
            director = None
        return director

    @classmethod
    def get_or_create_director(cls, search_data: dict) -> Optional[Director]:
        cls.check_source_urls(search_data=search_data)

        imdb_url = search_data.get("imdb_director_url")
        rt_url = search_data.get("rt_director_url")
        if imdb_url:
            director = cls.get_director(filter_map={"imdb_url": imdb_url})
            director_data = {
                "first_name": search_data["imdb_director"]["first_name"],
                "last_name": search_data["imdb_director"]["last_name"],
            }
        else:  # if url := search_data.get("rt_director_url"):
            director = cls.get_director(filter_map={"rt_url": rt_url})
            director_data = {
                "first_name": search_data["rt_director"]["first_name"],
                "last_name": search_data["rt_director"]["last_name"],
            }

        director_data.update({"rt_url": rt_url, "imdb_url": imdb_url})
        if not director:
            director = Director.objects.create(**director_data)

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
