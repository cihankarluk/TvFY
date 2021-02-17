from TvFY.actor.models import Actor
from TvFY.core.models import Country


class ActorService:
    def __init__(self, search_data: dict, actor_obj: Actor):
        self.search_data = search_data
        self.actor = actor_obj

    @staticmethod
    def get_or_create_country(country: str):
        if country:
            country, _ = Country.objects.get_or_create(country=country)
        return country

    def update_actor(self):
        born_at = self.search_data.pop("born_at", None)
        died_at = self.search_data.pop("died_at", None)
        for field, value in self.search_data.items():
            setattr(self.actor, field, value)
        self.actor.born_at = self.get_or_create_country(country=born_at)
        self.actor.died_at = self.get_or_create_country(country=died_at)
        self.actor.save()
