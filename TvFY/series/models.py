from django.db import models

from TvFY.artist.models import Artist
from TvFY.genre.models import Genre


class Series(models.Model):
    name = models.CharField(max_length=255)
    language = models.CharField(max_length=255, blank=True, null=True)
    imdb_rate = models.FloatField(blank=True, null=True)
    rotten_tomatoes_rate = models.FloatField(blank=True, null=True)
    subscription = models.CharField(max_length=255, blank=True, null=True)
    artists = models.ManyToManyField(Artist)
    run_time = models.IntegerField(blank=True, null=True)
    creator = models.CharField(max_length=128, blank=True, null=True)
    image = models.URLField(blank=True, null=True)
    storyline = models.TextField()
    genres = models.ManyToManyField(Genre)
    release_date = models.DateField()
    is_active = models.BooleanField()


class Episode(models.Model):
    name = models.CharField(max_length=255)
    imdb_rate = models.FloatField(blank=True, null=True)
    release_date = models.DateField()
    storyline = models.TextField()
