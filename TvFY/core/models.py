from django.db import models
from django.utils import timezone


class AuditMixin(models.Model):
    created_by = models.CharField(
        db_column="created_by", max_length=100, blank=True, editable=False, null=True
    )
    updated_by = models.CharField(
        db_column="updated_by", max_length=100, blank=True, null=True
    )
    created_at = models.DateTimeField(db_column="created_at", auto_now_add=True)
    updated_at = models.DateTimeField(db_column="updated_at", auto_now=True)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        from TvFY.core.helpers import get_current_user

        user = get_current_user()
        self.updated_at = timezone.now()
        if user:
            self.updated_by = user and user.username or None
        if not self.pk:
            self.created_at = self.updated_at
            self.created_by = self.updated_by

        super(AuditMixin, self).save(*args, **kwargs)


class ErrorReport(models.Model):
    error_code = models.CharField(max_length=128)
    error_description = models.CharField(max_length=255)
    is_ok = models.BooleanField(default=False)
    url = models.URLField()

    def __str__(self):
        return self.error_code


class Country(models.Model):
    country = models.CharField(max_length=255)


class Language(models.Model):
    language = models.CharField(max_length=128)
