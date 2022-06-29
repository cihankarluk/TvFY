from typing import Any, Optional

from TvFY.collector.base import Scraper
from TvFY.core.exceptions import NotAbleToFindDirectorSourceUrl
from TvFY.country.service import CountryService
from TvFY.director.models import Director


class DirectorService:
    @classmethod
    def check_source_urls(cls, search_data: dict[str, Any]):
        """At least one of them concur to find data about that movie."""
        if not (search_data.get("imdb_director_url") or search_data.get("rt_director_url")):
            raise NotAbleToFindDirectorSourceUrl(
                "Cannot find source url for that director. If you know address please contact."
            )

    @classmethod
    def get_director(cls, filter_map: dict[str, Any]) -> Optional[Director]:
        director = None
        director_query = Director.objects.filter(**filter_map)
        if director_query.exists():
            director = director_query.get()

        return director

    @classmethod
    def get_or_create_director(cls, search_data: dict[str, Any]) -> Optional[Director]:
        """This method only initialize director."""
        cls.check_source_urls(search_data=search_data)

        rt_url = search_data.get("rt_director_url")
        if imdb_url := search_data.get("imdb_director_url"):
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
    def update_director(cls, director_obj: Director, director_data: dict[str, Any]):
        if born_at := director_data.pop("born_at", None):
            director_obj.born_at = CountryService.get_or_create_country(country_name=born_at)
        if died_at := director_data.pop("died_at", None):
            director_obj.died_at = CountryService.get_or_create_country(country_name=died_at)
        for field, value in director_data.items():
            setattr(director_obj, field, value)
        director_obj.is_updated = True
        director_obj.save()

    @classmethod
    def scrap_and_update_director(cls):
        directors = Director.objects.filter(is_updated=False)

        director_map = {director.imdb_url: director for director in directors}
        urls = list(director_map.keys())
        results = Scraper(urls=urls).handle()

        for imdb_url, data in results.items():
            cls.update_director(director_obj=director_map[imdb_url], director_data=data)
