from django.db import models

from TvFY.core.models import Country


class Director(models.Model):
    first_name = models.CharField(max_length=128)
    last_name = models.CharField(max_length=128)
    imdb_url = models.URLField(blank=True, null=True, unique=True)
    rt_url = models.URLField(blank=True, null=True, unique=True)
    born = models.DateField(null=True)
    born_at = models.ForeignKey(
        Country, on_delete=models.SET_NULL, null=True, related_name="born_place"
    )
    died = models.DateField(null=True)
    died_at = models.ForeignKey(
        Country, on_delete=models.SET_NULL, null=True, related_name="death_place"
    )
    perks = models.CharField(max_length=255, null=True)
    oscars = models.PositiveSmallIntegerField(default=0)
    oscar_nominations = models.PositiveSmallIntegerField(default=0)
    wins = models.PositiveSmallIntegerField(blank=True, null=True, default=0)
    nominations = models.PositiveSmallIntegerField(blank=True, null=True, default=0)

    @property
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return self.get_full_name
