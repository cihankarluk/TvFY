from django.contrib.postgres.fields import ArrayField
from django.db import models

from TvFY.core.models import Country


class Actor(models.Model):
    first_name = models.CharField(max_length=128)
    last_name = models.CharField(max_length=128)
    imdb_url = models.URLField(blank=True, null=True, unique=True)
    born_date = models.DateField(null=True)
    born_at = models.ForeignKey(
        Country, on_delete=models.SET_NULL, null=True, related_name="actor_born_at"
    )
    died_date = models.DateField(null=True)
    died_at = models.ForeignKey(
        Country, on_delete=models.SET_NULL, null=True, related_name="actor_died_at"
    )
    perks = ArrayField(models.CharField(max_length=32, blank=True), null=True)
    oscars = models.PositiveSmallIntegerField(default=0)
    oscar_nominations = models.PositiveSmallIntegerField(default=0)
    wins = models.PositiveSmallIntegerField(blank=True, null=True, default=0)
    nominations = models.PositiveSmallIntegerField(blank=True, null=True, default=0)

    @property
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def actor_born_at(self):
        if country := self.born_at:
            country = self.born_at.country
        return country

    @property
    def actor_died_at(self):
        if country := self.died_at:
            country = self.died_at.country
        return country

    def __str__(self):
        return self.get_full_name
