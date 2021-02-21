from django.db import models

from TvFY.core.helpers import get_random_string


class SeriesManager(models.Manager):
    def create_series_code(self):
        code = get_random_string(12)
        series_code = f"{self.model.PREFIX}{code}"
        if super().get_queryset().filter(tvfy_code=series_code).exists():
            return self.create_series_code()
        return series_code

    def create(self, **series_data):
        series_data.update({"tvfy_code": self.create_series_code()})
        series = super(SeriesManager, self).create(**series_data)
        return series
