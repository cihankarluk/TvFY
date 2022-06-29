from typing import Optional

from django.contrib.postgres.fields import ArrayField
from django.db import models

from TvFY.core.models import AuditMixin
from TvFY.country.models import Country
from TvFY.director.managers import DirectorManager


class Director(AuditMixin):
    TYPE = "director"
    PREFIX = "dt"

    tvfy_code = models.CharField(db_column="tvfy", max_length=11, db_index=True, unique=True)
    first_name = models.CharField(db_column="first_name", max_length=128)
    last_name = models.CharField(db_column="last_name", max_length=128)
    full_name = models.CharField(db_column="full_name", max_length=255)
    imdb_url = models.URLField(db_column="imdb_url", null=True, unique=True)
    rt_url = models.URLField(db_column="rt_url", null=True, unique=True)
    born_date = models.DateTimeField(db_column="born_date", null=True)
    born_at = models.ForeignKey(
        Country,
        db_column="born_at",
        on_delete=models.SET_NULL,
        null=True,
        related_name="d_born_at",
    )
    died_date = models.DateTimeField(db_column="died_date", null=True)
    died_at = models.ForeignKey(
        Country,
        db_column="died_at",
        on_delete=models.SET_NULL,
        null=True,
        related_name="d_died_at",
    )
    perks = ArrayField(
        models.CharField(db_column="perks", max_length=32, blank=True),
        null=True,
    )
    oscars = models.PositiveSmallIntegerField(db_column="oscars", null=True)
    oscar_nominations = models.PositiveSmallIntegerField(db_column="oscar_nominations", null=True)
    wins = models.PositiveSmallIntegerField(db_column="wins", null=True)
    nominations = models.PositiveSmallIntegerField(db_column="nominations", null=True)
    is_updated = models.BooleanField(db_column="is_updated", default=False)

    objects = DirectorManager()

    @property
    def director_born_at(self) -> Optional[str]:
        return self.born_at.name if self.born_at else None

    @property
    def director_died_at(self) -> Optional[str]:
        return self.died_at.name if self.died_at else None

    def __str__(self):
        return self.full_name
