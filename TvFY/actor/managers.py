from typing import Union

from django.db import models

from TvFY.core.helpers import get_random_string


class ActorManager(models.Manager):
    @property
    def create_actor_code(self) -> Union[str, classmethod]:
        actor_code = f"{self.model.PREFIX}-{get_random_string(8)}"
        if super().get_queryset().filter(tvfy_code=actor_code).exists():
            return self.create_actor_code()
        return actor_code

    def create(self, **actor_data):
        actor_data.update({"tvfy_code": self.create_actor_code})
        actor_data.update({"full_name": f"{actor_data['first_name']} {actor_data['last_name']}"})
        actor = super(ActorManager, self).create(**actor_data)
        return actor
