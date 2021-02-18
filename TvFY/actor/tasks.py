from TvFY.actor.models import Actor
from TvFY.actor.service import ActorService
from TvFY.collector.base import Scrapper


def fill_actor_data():
    actors = Actor.objects.filter(born_date__isnull=True)
    for actor in actors:
        cls = Scrapper(urls=actor.imdb_url)
        result = cls.handle()
        service = ActorService(search_data=result, actor_obj=actor)
        service.update_actor()
