from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from TvFY.core.models import AuditMixin
from TvFY.movies.models import Movie
from TvFY.series.models import Season, Series


class Account(AbstractUser):
    email = models.EmailField(_("email address"), unique=True)

    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")
        db_table = "account"

    def get_display_name(self):
        return self.username or self.email


class UserMovies(AuditMixin):
    user = models.ForeignKey(
        to=Account,
        db_column="user",
        on_delete=models.CASCADE,
    )
    movie = models.ForeignKey(
        to=Movie,
        to_field="tvfy_code",
        db_column="movie",
        on_delete=models.CASCADE,
    )

    is_watched = models.BooleanField(db_column="is_watched")
    is_going_to_watch = models.BooleanField(db_column="is_going_to_watch")

    def __str__(self):
        return f"{self.user.username} -> {self.movie.title}"


class UserSeries(AuditMixin):
    user = models.ForeignKey(
        to=Account,
        db_column="user",
        on_delete=models.CASCADE,
    )
    series = models.ForeignKey(
        to=Series,
        to_field="tvfy_code",
        db_column="series",
        on_delete=models.CASCADE,
    )
    watched_season = models.ForeignKey(
        to=Season,
        db_column="watched_season",
        on_delete=models.CASCADE,
    )

    last_watched_episode = models.PositiveSmallIntegerField(db_column="last_watched_episode", null=True)

    is_watched = models.BooleanField(db_column="is_watched")
    is_going_to_watch = models.BooleanField(db_column="is_going_to_watch")

    class Meta:
        unique_together = ["user", "series", "watched_season"]

    def __str__(self):
        return f"{self.user.username} -> {self.series.title} / {self.watched_season.season}"
