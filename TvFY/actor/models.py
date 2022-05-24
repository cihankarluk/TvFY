from django.contrib.postgres.fields import ArrayField
from django.db import models

from TvFY.actor.managers import ActorManager
from TvFY.core.models import AuditMixin
from TvFY.country.models import Country


class Actor(AuditMixin):
    TYPE = "actor"
    PREFIX = "ac"

    tvfy_code = models.CharField(max_length=11, db_index=True, unique=True)
    first_name = models.CharField(max_length=128)
    last_name = models.CharField(max_length=128)
    full_name = models.CharField(max_length=255, db_index=True)
    imdb_url = models.URLField(unique=True)
    born_date = models.DateTimeField(null=True)
    born_at = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True, related_name="a_born_at")
    died_date = models.DateTimeField(null=True)
    died_at = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True, related_name="a_died_at")
    perks = ArrayField(models.CharField(max_length=32), null=True)
    oscars = models.PositiveSmallIntegerField(null=True)
    oscar_nominations = models.PositiveSmallIntegerField(null=True)
    wins = models.PositiveSmallIntegerField(null=True)
    nominations = models.PositiveSmallIntegerField(null=True)
    is_updated = models.BooleanField(default=False)

    objects = ActorManager()

    @property
    def actor_born_at(self):
        if country := self.born_at:
            country = self.born_at.name
        return country

    @property
    def actor_died_at(self):
        if country := self.died_at:
            country = self.died_at.name
        return country

    def __str__(self):
        return self.full_name
