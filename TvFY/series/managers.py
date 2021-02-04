from django.db import models

from TvFY.actor.models import Actor
from TvFY.core.helpers import get_random_string
from TvFY.core.models import Country, Language
from TvFY.genre.models import Genre


class SeriesManager(models.Manager):
    @staticmethod
    def get_genres(series_data):
        genres = set(series_data.pop("rt_genre", {}))
        genres.update(set(series_data.pop("imdb_genre", {})))
        genre_ids = Genre.objects.filter(name__in=genres).values_list("id", flat=True)
        return genre_ids

    @staticmethod
    def get_or_create_language(series_data):
        languages: list = series_data.pop("language", [])
        language_objs = []
        for language in languages:
            language_obj, _ = Language.objects.get_or_create(language=language)
            language_objs.append(language_obj)
        return language_objs

    @staticmethod
    def get_or_create_country(series_data):
        countries: list = series_data.pop("country", [])
        country_objs = []
        for country in countries:
            country_obj, _ = Country.objects.get_or_create(country=country)
            country_objs.append(country_obj)
        return country_objs

    def create_series_code(self):
        from TvFY.series.models import Series

        code = get_random_string(8)
        series_code = f"{Series.PREFIX}{code}"
        if super().get_queryset().filter(tvfy_code=series_code).exists():
            return self.create_series_code()
        return series_code

    def save_series(self, **series_data):
        series_data.update({"tvfy_code": self.create_series_code()})
        genres = self.get_genres(series_data)
        languages = self.get_or_create_language(series_data)
        countries = self.get_or_create_country(series_data)
        series = self.create(**series_data)
        for genre in genres:
            series.genres.add(genre)
        for language in languages:
            series.language.add(language)
        for country in countries:
            series.country.add(country)
        return series


class SeriesCastManager(models.Manager):
    @staticmethod
    def get_or_create_actor(actor_data):
        actor, _ = Actor.objects.get_or_create(
            first_name=actor_data["first_name"], last_name=actor_data["last_name"]
        )
        return actor

    def save_series_cast(self, series, cast_data):
        from TvFY.series.models import SeriesCast

        series_cast = []
        for cast in cast_data:
            actor = self.get_or_create_actor(cast)
            series_cast.append(
                SeriesCast(
                    character_name=cast["character_name"],
                    episode_count=cast["episode_count"],
                    start_acting=cast["start_acting"],
                    end_acting=cast["end_acting"],
                    series=series,
                    actor=actor,
                )
            )
        self.bulk_create(series_cast)
