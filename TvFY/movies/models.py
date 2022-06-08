from django.db import models

from TvFY.actor.models import Actor
from TvFY.core.models import AuditMixin
from TvFY.country.models import Country
from TvFY.director.models import Director
from TvFY.genre.models import Genre
from TvFY.language.models import Language
from TvFY.movies.managers import MovieManager


class Movie(AuditMixin):
    TYPE = "movie"
    PREFIX = "mv"

    tvfy_code = models.CharField(db_column="tvfy", max_length=11, unique=True, db_index=True)

    title = models.CharField(db_column="title", max_length=255)
    storyline = models.TextField(db_column="storyline", null=True)
    release_date = models.DateTimeField(db_column="release_date", null=True)
    run_time = models.PositiveIntegerField(db_column="run_time", null=True)

    wins = models.PositiveIntegerField(db_column="wins", null=True)
    nominations = models.PositiveIntegerField(db_column="nominations", null=True)
    oscar_wins = models.PositiveIntegerField(db_column="oscar_wins", null=True)
    oscar_nominations = models.PositiveIntegerField(db_column="oscar_nominations", null=True)

    imdb_rate = models.FloatField(db_column="imdb_rate", null=True)
    imdb_vote_count = models.PositiveIntegerField(db_column="imdb_vote_count", null=True)
    imdb_popularity = models.PositiveIntegerField(db_column="imdb_popularity", null=True)
    imdb_url = models.URLField(db_column="imdb_url", null=True, unique=True, db_index=True)

    rt_tomatometer_rate = models.PositiveIntegerField(db_column="rt_tomatometer_rate", null=True)
    rt_audience_rate = models.PositiveIntegerField(db_column="rt_audience_rate", null=True)
    rotten_tomatoes_url = models.URLField(db_column="rotten_tomatoes_url", null=True, unique=True, db_index=True)

    budget_amount = models.PositiveIntegerField(db_column="budget_amount", null=True)
    budget_currency = models.CharField(db_column="budget_currency", max_length=3, null=True)
    usa_ow_amount = models.PositiveIntegerField(db_column="usa_ow_amount", null=True)
    usa_ow_currency = models.CharField(db_column="usa_ow_currency", max_length=3, null=True)
    ww_amount = models.PositiveIntegerField(db_column="ww_amount", null=True)
    ww_currency = models.CharField(db_column="ww_currency", max_length=3, null=True)

    metacritic_score = models.PositiveIntegerField(db_column="metacritic_score", null=True)

    director = models.ForeignKey(to=Director, db_column="director", on_delete=models.CASCADE, null=True)
    genres = models.ManyToManyField(to=Genre, db_column="genres")
    country = models.ManyToManyField(to=Country, db_column="country")
    language = models.ManyToManyField(to=Language, db_column="language")

    objects = MovieManager()

    def __str__(self):
        return self.title


class MovieCast(models.Model):
    character_name = models.CharField(db_column="character_name", max_length=255, default="John Doe")

    movie = models.ForeignKey(to=Movie, db_column="movie", on_delete=models.CASCADE)
    actor = models.ForeignKey(to=Actor, db_column="actor", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.character_name} ({self.actor.first_name} {self.actor.last_name})"
