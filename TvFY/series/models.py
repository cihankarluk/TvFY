from django.contrib.postgres.fields import ArrayField
from django.db import models

from TvFY.actor.models import Actor
from TvFY.core.models import AuditMixin
from TvFY.country.models import Country
from TvFY.director.models import Director
from TvFY.genre.models import Genre
from TvFY.language.models import Language
from TvFY.series.managers import SeriesManager, SeriesCastManager, SeriesEpisodeCastManager, SeriesSeasonManager


class Series(AuditMixin):
    TYPE = "series"
    PREFIX = "sr"

    tvfy_code = models.CharField(db_column="tvfy_code", max_length=11, db_index=True, unique=True)

    title = models.CharField(db_column="title", max_length=255)
    storyline = models.TextField(db_column="storyline", null=True)
    release_date = models.DateTimeField(db_column="release_date", null=True)
    end_date = models.DateTimeField(db_column="end_date", null=True)
    run_time = models.IntegerField(db_column="run_time", null=True)

    is_active = models.BooleanField(db_column="is_active", null=True)
    season_count = models.IntegerField(db_column="season_count", null=True)
    wins = models.IntegerField(db_column="wins", null=True)
    nominations = models.IntegerField(db_column="nominations", null=True)
    tv_network = ArrayField(models.CharField(max_length=32), db_column="tv_network", null=True)

    imdb_rate = models.FloatField(db_column="imdb_rate", null=True)
    imdb_vote_count = models.IntegerField(db_column="imdb_vote_count", null=True)
    imdb_popularity = models.IntegerField(db_column="imdb_popularity", null=True)
    imdb_url = models.URLField(db_column="imdb_url", null=True)

    rt_tomatometer_rate = models.IntegerField(db_column="rt_tomatometer_rate", null=True)
    rt_audience_rate = models.IntegerField(db_column="rt_audience_rate", null=True)
    rotten_tomatoes_url = models.URLField(db_column="rotten_tomatoes_url", null=True)

    tv_com_rate = models.FloatField(db_column="tv_com_rate", null=True)
    tv_com_url = models.URLField(db_column="tv_com_url", null=True)

    creator = models.ForeignKey(to=Director, db_column="creator", on_delete=models.SET_NULL, null=True)
    genres = models.ManyToManyField(to=Genre, db_column="tvfy_code")
    country = models.ManyToManyField(to=Country, db_column="tvfy_code")
    language = models.ManyToManyField(to=Language, db_column="tvfy_code")

    objects = SeriesManager()

    class Meta:
        ordering = ("id",)

    def __str__(self):
        return self.title


class SeriesCast(models.Model):
    TYPE = "seriescast"
    PREFIX = "sc"

    tvfy_code = models.CharField(db_column="tvfy_code", max_length=11, db_index=True, unique=True)
    character_name = models.CharField(db_column="character_name", max_length=255)
    episode_count = models.IntegerField(db_column="episode_count", null=True)
    start_acting = models.DateTimeField(db_column="start_acting", null=True)
    end_acting = models.DateTimeField(db_column="end_acting", null=True)

    series = models.ForeignKey(to=Series, db_column="series", on_delete=models.CASCADE)
    actor = models.ForeignKey(to=Actor, db_column="actor", on_delete=models.CASCADE)

    objects = SeriesCastManager()

    def __str__(self):
        return f"{self.character_name} ({self.actor.first_name} {self.actor.last_name})"


class Season(models.Model):
    TYPE = "season"
    PREFIX = "se"

    tvfy_code = models.CharField(db_column="tvfy_code", max_length=11, db_index=True, unique=True)
    season = models.CharField(db_column="season", max_length=3)
    imdb_url = models.URLField(db_column="imdb_url")
    imdb_season_average_rate = models.FloatField(db_column="imdb_season_average_rate", null=True)

    series = models.ForeignKey(to=Series, db_column="series", on_delete=models.CASCADE)

    objects = SeriesSeasonManager()

    def __str__(self):
        return f"{self.season}: {self.series.title}"


class Episode(models.Model):
    TYPE = "episode"
    PREFIX = "ep"

    tvfy_code = models.CharField(db_column="tvfy_code", max_length=11, db_index=True, unique=True)
    title = models.CharField(db_column="title", max_length=255)
    storyline = models.TextField(db_column="storyline", null=True)
    release_date = models.DateField(db_column="release_date", null=True)
    imdb_rate = models.FloatField(db_column="imdb_rate", null=True)
    imdb_vote_count = models.IntegerField(db_column="imdb_vote_count", null=True)
    episode = models.IntegerField(db_column="episode", null=True)

    season = models.ForeignKey(to=Season, db_column="season", on_delete=models.CASCADE)

    objects = SeriesEpisodeCastManager()

    class Meta:
        unique_together = [("episode", "season")]

    def __str__(self):
        return self.title
