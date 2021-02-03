from django.db.models.signals import post_save
from django.dispatch import receiver

from TvFY.series.models import Episode


@receiver(post_save, sender=Episode)
def calculate_imdb_average_rate(instance, **kwargs):
    imdb_rate = instance.imdb_rate
    season_rate = instance.season.imdb_season_average_rate
    if season_rate:
        avg_rate = round((imdb_rate + season_rate) / 2)
        instance.season.imdb_season_average_rate = avg_rate
        instance.season.save()
    else:
        instance.season.imdb_season_average_rate = imdb_rate
        instance.season.save()
