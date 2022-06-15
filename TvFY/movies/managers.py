from django.db import models

from TvFY.core.managers import ManagerMixin


class MovieManager(ManagerMixin, models.Manager):

    def create(self, **movie_data):
        movie_data.update({"tvfy_code": self.create_tvfy_code()})
        movie = super(MovieManager, self).create(**movie_data)
        return movie
