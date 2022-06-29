from django.db import models

from TvFY.core.managers import ManagerMixin


class ActorManager(ManagerMixin, models.Manager):
    def create(self, **actor_data):
        actor_data.update({"tvfy_code": self.create_tvfy_code()})
        actor_data.update({"full_name": f"{actor_data['first_name']} {actor_data['last_name']}"})
        actor = super().create(**actor_data)
        return actor
