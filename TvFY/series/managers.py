from django.db import models, transaction, IntegrityError
from django.db.models.utils import resolve_callables

from TvFY.core.managers import ManagerMixin


class SeriesManager(ManagerMixin, models.Manager):

    def create(self, **series_data):
        series_data.update({"tvfy_code": self.create_tvfy_code()})
        series = super(SeriesManager, self).create(**series_data)
        return series


class SeriesCastManager(ManagerMixin, models.Manager):

    def create(self, **cast_data):
        cast_data.update({"tvfy_code": self.create_tvfy_code()})
        series = super(SeriesCastManager, self).create(**cast_data)
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
