from django.db import models

from TvFY.core.helpers import get_random_string


class MovieManager(models.Manager):
    @property
    def create_movie_code(self):
        movie_code = f"{self.model.PREFIX}-{get_random_string(11)}"
        if super().get_queryset().filter(tvfy_code=movie_code).exists():
            return self.create_series_code()
        return movie_code

    def create(self, **movie_data):
        movie_data.update({"tvfy_code": self.create_movie_code})
        movie = super(MovieManager, self).create(**movie_data)
        return movie
