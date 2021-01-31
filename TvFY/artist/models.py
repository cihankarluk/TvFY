from django.db import models


class Artist(models.Model):
    first_name = models.CharField(max_length=128)
    last_name = models.CharField(max_length=128)
    image = models.URLField(null=True, blank=True)
    awards = models.IntegerField(default=0)
