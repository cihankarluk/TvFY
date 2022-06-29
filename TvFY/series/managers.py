from django.db import models

from TvFY.core.managers import ManagerMixin


class SeriesManager(ManagerMixin, models.Manager):
    def create(self, **series_data):
        series_data.update({"tvfy_code": self.create_tvfy_code()})
        series = super().create(**series_data)
        return series


class SeriesCastManager(ManagerMixin, models.Manager):
    def create(self, **cast_data):
        cast_data.update({"tvfy_code": self.create_tvfy_code()})
        series = super().create(**cast_data)
        return series


class SeriesSeasonManager(ManagerMixin, models.Manager):
    def create(self, **season_data):
        season_data.update({"tvfy_code": self.create_tvfy_code()})
        series = super().create(**season_data)
        return series


class SeriesEpisodeCastManager(ManagerMixin, models.Manager):
    def create(self, **episode_data):
        episode_data.update({"tvfy_code": self.create_tvfy_code()})
        series = super().create(**episode_data)
        return series
