from typing import List

from TvFY.actor.models import Actor
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
    def update_actor(cls, actor_data: dict, actor: Actor):
        born_at = actor_data.pop("born_at", None)
        died_at = actor_data.pop("died_at", None)
        for field, value in actor_data.items():
            setattr(actor, field, value)
        actor.born_at = CountryService.get_or_create_country(country_name=born_at)
        actor.died_at = CountryService.get_or_create_country(country_name=died_at)
        actor.save()
