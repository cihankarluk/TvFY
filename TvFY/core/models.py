from django.db import models
from django.utils import timezone


class AuditMixin(models.Model):
    created_by = models.CharField(
        db_column="created_by",
        max_length=100,
        blank=True,
        editable=False,
        null=True,
    )
    updated_by = models.CharField(db_column="updated_by", max_length=100, blank=True, null=True)
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

        super().save(*args, **kwargs)
