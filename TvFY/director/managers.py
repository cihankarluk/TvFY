from typing import Union

from django.db import models

from TvFY.core.helpers import get_random_string


class DirectorManager(models.Manager):

    @property
    def create_director_code(self) -> Union[str, classmethod]:
        director_code = f"{self.model.PREFIX}-{get_random_string(8)}"
        if super().get_queryset().filter(tvfy_code=director_code).exists():
            return self.create_director_code()
        return director_code

    def create(self, **director_data):
        director_data.update({"tvfy_code": self.create_director_code})
        director_data.update({"full_name": f"{director_data['first_name']} {director_data['last_name']}"})
        director = super(DirectorManager, self).create(**director_data)
        return director
