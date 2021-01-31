from django.db import models

from TvFY.artist.models import Artist
from TvFY.core.helpers import get_random_string
from TvFY.core.models import Country, Language
from TvFY.genre.models import Genre


class SeriesManager(models.Manager):
    @staticmethod
    def get_genres(series_data):
        genres = set(series_data.pop("rt_genre", {}))
        genres.update(set(series_data.pop("imdb_genre", {})))
        genre_ids = Genre.objects.filter(
            name__in=genres
        ).values_list(
            'id', flat=True
        )
        return genre_ids

    def create_series_code(self):
        code = get_random_string(8)
        series_code = f'{Series.PREFIX}{code}'
        if super().get_queryset().filter(tvfy_code=series_code).exists():
            return self.create_series_code()
        return series_code

    def save_series(self, **series_data):
        series_data.update({'tvfy_code': self.create_series_code()})
        genres = self.get_genres(series_data)
        series = self.create(**series_data)
        for genre in genres:
            series.genres.add(genre)
        return series


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

    image = models.URLField(blank=True, null=True)
    imdb_url = models.URLField(blank=True, null=True)
    tv_network_url = models.URLField(blank=True, null=True)
    rotten_tomatoes_url = models.URLField(blank=True, null=True)

    genres = models.ManyToManyField(Genre)
    country = models.ManyToManyField(Country)
    language = models.ManyToManyField(Language)

    objects = SeriesManager()

    def __str__(self):
        return self.name


class SeriesArtist(models.Model):
    artists = models.ManyToManyField(Artist)
    character_name = models.CharField(max_length=255, default="John Doe")
    episode_count = models.IntegerField(default=0)
    start_acting = models.DateField(blank=True, null=True)
    end_acting = models.DateField(blank=True, null=True)

    series = models.ForeignKey(Series, on_delete=models.CASCADE)


class Season(models.Model):
    season = models.IntegerField()
    imdb_url = models.URLField(blank=True, null=True)
    imdb_season_average_rate = models.FloatField(blank=True, null=True)
    tvfy_rate = models.FloatField(blank=True, null=True)

    series = models.ForeignKey(Series, on_delete=models.CASCADE)


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
