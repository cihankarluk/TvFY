from django.contrib.postgres.fields import ArrayField
from django.db import models

from TvFY.actor.managers import ActorManager
from TvFY.core.models import AuditMixin
from TvFY.country.models import Country


class Actor(AuditMixin):
    TYPE = "actor"
    PREFIX = "ac"

    tvfy_code = models.CharField(db_column="tvfy", max_length=11, db_index=True, unique=True)
    first_name = models.CharField(db_column="first_name", max_length=128)
    last_name = models.CharField(db_column="last_name", max_length=128)
    full_name = models.CharField(db_column="full_name", max_length=255, db_index=True)
    imdb_url = models.URLField(db_column="imdb_url", unique=True)
    born_date = models.DateTimeField(db_column="born_date", null=True)
    born_at = models.ForeignKey(to=Country, db_column="born_at", on_delete=models.SET_NULL, null=True,
                                related_name="a_born_at")
    died_date = models.DateTimeField(db_column="died_date", null=True)
    died_at = models.ForeignKey(to=Country, db_column="died_at", on_delete=models.SET_NULL, null=True,
                                related_name="a_died_at")
    perks = ArrayField(models.CharField(db_column="perks", max_length=32), null=True)
    oscars = models.PositiveSmallIntegerField(db_column="oscars", null=True)
    oscar_nominations = models.PositiveSmallIntegerField(db_column="oscar_nominations", null=True)
    wins = models.PositiveSmallIntegerField(db_column="wins", null=True)
    nominations = models.PositiveSmallIntegerField(db_column="nominations", null=True)
    is_updated = models.BooleanField(db_column="is_updated", default=False)

    objects = ActorManager()

    @property
    def actor_born_at(self):
        return self.born_at.name if self.born_at else None

    @property
    def actor_died_at(self):
        return self.died_at.name if self.died_at else None

    def __str__(self):
        return self.full_name
