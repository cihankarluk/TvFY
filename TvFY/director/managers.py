from django.db import models

from TvFY.core.managers import ManagerMixin


class DirectorManager(ManagerMixin, models.Manager):
    def create(self, **director_data):
        director_data.update({"tvfy_code": self.create_tvfy_code()})
        director_data.update({"full_name": f"{director_data['first_name']} {director_data['last_name']}"})
        director = super().create(**director_data)
        return director
