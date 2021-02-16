from TvFY.collector.base import Scrapper
from TvFY.director.models import Director
from TvFY.director.service import DirectorService


def fill_director_data():
    directors = Director.objects.filter(born__isnull=True)
    for director in directors:
        cls = Scrapper(urls=director.imdb_url)
        result = cls.handle()
        service = DirectorService(search_data=result, director_obj=director)
        service.update_director()
