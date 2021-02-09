from django.db import models


class Director(models.Model):
    first_name = models.CharField(max_length=128)
    last_name = models.CharField(max_length=128)
    imdb_url = models.URLField(blank=True, null=True)
    rt_url = models.URLField(blank=True, null=True)
    born = models.DateField(null=True)
    born_at = models.CharField(max_length=255, null=True)
    died = models.DateField(null=True)
    died_at = models.CharField(max_length=255, null=True)
    hits = models.CharField(max_length=255, null=True)
    wins = models.IntegerField(blank=True, null=True, default=0)
    nominations = models.IntegerField(blank=True, null=True, default=0)

    @property
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return self.get_full_name
