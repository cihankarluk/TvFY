from typing import List

from TvFY.actor.models import Actor
from TvFY.collector.base import Scraper
from TvFY.country.service import CountryService


class ActorService:

    @classmethod
    def create_actor(cls, actor_data: dict) -> Actor:
        actor = Actor.objects.create(
            first_name=actor_data["first_name"],
            last_name=actor_data["last_name"],
            imdb_url=actor_data["imdb_actor_url"],
        )
        return actor

    @classmethod
    def create_multiple_actor(cls, cast_data: List[dict]) -> dict:
        """
        Creates multiple actors.
        """
        cast_dict = {cast["imdb_actor_url"]: cast for cast in cast_data}
        existing_actors = Actor.objects.filter(imdb_url__in=list(cast_dict.keys()))

        for key, value in cast_dict.items():
            if actor := existing_actors.filter(imdb_url=key):
                value["actor"] = actor.get()
            else:
                value["actor"] = cls.create_actor(value)
        return cast_dict

    @classmethod
    def update_actor(cls, actor_obj: Actor, actor_data: dict):
        if born_at := actor_data.pop("born_at", None):
            actor_obj.born_at = CountryService.get_or_create_country(country_name=born_at)
        if died_at := actor_data.pop("died_at", None):
            actor_obj.died_at = CountryService.get_or_create_country(country_name=died_at)
        for field, value in actor_data.items():
            setattr(actor_obj, field, value)
        actor_obj.save()

    @classmethod
    def scrap_and_update_actor(cls):
        actors = Actor.objects.filter(is_updated=False)

        actor_map = {actor.imdb_url: actor for actor in actors}
        urls = list(actor_map.keys())

        results = Scraper(urls=urls).handle()

        for imdb_url, data in results.items():
            cls.update_actor(actor_obj=actor_map[imdb_url], actor_data=data)
