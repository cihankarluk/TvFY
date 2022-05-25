from django.db import models


class Genre(models.Model):
    name = models.CharField(db_column="name", max_length=128)
    detail = models.TextField(db_column="detail")

    def __str__(self):
        return self.name
