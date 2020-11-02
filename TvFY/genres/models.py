from django.db import models


class Genres(models.Model):
    name = models.CharField(max_length=128)
