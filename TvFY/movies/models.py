from django.db import models

from TvFY.actor.models import Actor
from TvFY.core.models import Country, Language
from TvFY.director.models import Director
from TvFY.genre.models import Genre
from TvFY.movies.managers import MovieManager


class Movie(models.Model):
    TYPE = "movie"
    PREFIX = "MV"

    tvfy_code = models.CharField(max_length=10, db_index=True)

    name = models.CharField(max_length=255)
    creator = models.CharField(max_length=128, blank=True, null=True)
    storyline = models.TextField()
    release_date = models.DateField(blank=True, null=True)
    run_time = models.PositiveIntegerField(blank=True, null=True)
    rt_tomatometer = models.PositiveIntegerField(blank=True, null=True)
    rt_tomatometer_count = models.PositiveIntegerField(blank=True, null=True)
    rt_audience_rate = models.PositiveIntegerField(blank=True, null=True)
    rt_audience_rate_count = models.PositiveIntegerField(blank=True, null=True)
    imdb_popularity = models.PositiveIntegerField(blank=True, null=True)
    imdb_rate = models.FloatField(blank=True, null=True)
    imdb_vote_count = models.PositiveIntegerField(blank=True, null=True)
    wins = models.PositiveIntegerField(blank=True, null=True, default=0)
    nominations = models.PositiveIntegerField(blank=True, null=True, default=0)
    budget = models.PositiveIntegerField(blank=True, null=True, default=0)
    usa_opening_weekend = models.PositiveIntegerField(blank=True, null=True, default=0)
    ww_gross = models.PositiveIntegerField(blank=True, null=True, default=0)
    imdb_url = models.URLField(blank=True, null=True)
    rotten_tomatoes_url = models.URLField(blank=True, null=True)

    director = models.ForeignKey(Director, on_delete=models.CASCADE)
    genres = models.ManyToManyField(Genre)
    country = models.ManyToManyField(Country)
    language = models.ManyToManyField(Language)

    objects = MovieManager()

    def __str__(self):
        return self.name


class MovieCast(models.Model):
    character_name = models.CharField(max_length=255, default="John Doe")

    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    actor = models.ForeignKey(Actor, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.character_name} ({self.actor.first_name} {self.actor.last_name})"
