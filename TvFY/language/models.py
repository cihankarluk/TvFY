from django.db import models


class Language(models.Model):
    name = models.CharField(db_column="name", max_length=255)

    def __str__(self):
        return self.name
