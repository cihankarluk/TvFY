from django.db import models

from TvFY.actor.models import Actor
from TvFY.core.models import Country, Language
from TvFY.genre.models import Genre
from TvFY.series.managers import SeriesManager


class Series(models.Model):
    TYPE = "series"
    PREFIX = "SR"

    tvfy_code = models.CharField(max_length=14)
    name = models.CharField(max_length=255)

    creator = models.CharField(max_length=128, blank=True, null=True)

    run_time = models.IntegerField(blank=True, null=True)

    storyline = models.TextField()

    release_date = models.DateField()
    is_active = models.BooleanField()
    end_date = models.DateField(blank=True, null=True)

    tv_network = models.CharField(max_length=255, blank=True, null=True)

    wins = models.IntegerField(blank=True, null=True, default=0)
    nominations = models.IntegerField(blank=True, null=True, default=0)

    season_count = models.IntegerField(blank=True, null=True)

    imdb_rate = models.FloatField(blank=True, null=True)
    imdb_vote_count = models.IntegerField(blank=True, null=True)
    imdb_popularity = models.CharField(max_length=4, blank=True, null=True)
    tv_com_rate = models.FloatField(blank=True, null=True)
    rt_tomatometer = models.IntegerField(blank=True, null=True)
    rt_audience_rate = models.IntegerField(blank=True, null=True)
    tvfy_rate = models.FloatField(blank=True, null=True)
    tvfy_popularity = models.FloatField(blank=True, null=True)

    imdb_url = models.URLField(blank=True, null=True)
    tv_network_url = models.URLField(blank=True, null=True)
    rotten_tomatoes_url = models.URLField(blank=True, null=True)

    genres = models.ManyToManyField(Genre)
    country = models.ManyToManyField(Country)
    language = models.ManyToManyField(Language)

    objects = SeriesManager()

    def __str__(self):
        return self.name


class SeriesCast(models.Model):
    character_name = models.CharField(max_length=255, default="John Doe")
    episode_count = models.IntegerField(default=0)
    start_acting = models.DateField(blank=True, null=True)
    end_acting = models.DateField(blank=True, null=True)

    series = models.ForeignKey(Series, on_delete=models.CASCADE)
    actor = models.ForeignKey(Actor, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.character_name} ({self.actor.first_name} {self.actor.last_name})"


class Season(models.Model):
    season = models.IntegerField()
    imdb_url = models.URLField(blank=True, null=True)
    imdb_season_average_rate = models.FloatField(blank=True, null=True)
    tvfy_rate = models.FloatField(blank=True, null=True)

    series = models.ForeignKey(Series, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.series.name}_{self.season}"


class Episode(models.Model):
    name = models.CharField(max_length=255)
    storyline = models.TextField(blank=True, null=True)
    release_date = models.DateField()
    imdb_rate = models.FloatField(blank=True, null=True)
    imdb_vote_count = models.IntegerField(default=0)
    tvfy_rate = models.FloatField(blank=True, null=True)
    tvfy_vote_count = models.FloatField(default=0)
    episode = models.IntegerField(default=0)

    season = models.ForeignKey(Season, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
