from django.db import models


class Actor(models.Model):
    first_name = models.CharField(max_length=128)
    last_name = models.CharField(max_length=128)
    awards = models.IntegerField(default=0)

    def __str__(self):
        return self.get_full_name

    @property
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"
