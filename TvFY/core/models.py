from django.db import models


class ErrorReport(models.Model):
    error_code = models.CharField(max_length=128)
    error_description = models.CharField(max_length=255)
    is_ok = models.BooleanField(default=False)
    url = models.URLField()

    def __str__(self):
        return self.error_code


class Country(models.Model):
    country = models.CharField(max_length=128)


class Language(models.Model):
    language = models.CharField(max_length=128)
