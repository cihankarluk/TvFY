# Generated by Django 4.0.4 on 2022-06-23 15:34

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("actor", "0001_initial"),
        ("country", "0001_initial"),
        ("genre", "0001_initial"),
        ("director", "0001_initial"),
        ("language", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Series",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created_by",
                    models.CharField(
                        blank=True,
                        db_column="created_by",
                        editable=False,
                        max_length=100,
                        null=True,
                    ),
                ),
                (
                    "updated_by",
                    models.CharField(
                        blank=True,
                        db_column="updated_by",
                        max_length=100,
                        null=True,
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(auto_now_add=True, db_column="created_at"),
                ),
                (
                    "updated_at",
                    models.DateTimeField(auto_now=True, db_column="updated_at"),
                ),
                (
                    "tvfy_code",
                    models.CharField(
                        db_column="tvfy_code",
                        db_index=True,
                        max_length=11,
                        unique=True,
                    ),
                ),
                ("title", models.CharField(db_column="title", max_length=255)),
                (
                    "storyline",
                    models.TextField(db_column="storyline", null=True),
                ),
                (
                    "release_date",
                    models.DateTimeField(db_column="release_date", null=True),
                ),
                (
                    "end_date",
                    models.DateTimeField(db_column="end_date", null=True),
                ),
                (
                    "run_time",
                    models.PositiveIntegerField(db_column="run_time", null=True),
                ),
                (
                    "is_active",
                    models.BooleanField(db_column="is_active", null=True),
                ),
                (
                    "season_count",
                    models.PositiveIntegerField(db_column="season_count", null=True),
                ),
                (
                    "wins",
                    models.PositiveIntegerField(db_column="wins", null=True),
                ),
                (
                    "nominations",
                    models.PositiveIntegerField(db_column="nominations", null=True),
                ),
                (
                    "oscar_wins",
                    models.PositiveIntegerField(db_column="oscar_wins", null=True),
                ),
                (
                    "oscar_nominations",
                    models.PositiveIntegerField(db_column="oscar_nominations", null=True),
                ),
                (
                    "tv_network",
                    models.CharField(db_column="tv_network", max_length=255, null=True),
                ),
                (
                    "imdb_rate",
                    models.FloatField(db_column="imdb_rate", null=True),
                ),
                (
                    "imdb_vote_count",
                    models.PositiveIntegerField(db_column="imdb_vote_count", null=True),
                ),
                (
                    "imdb_popularity",
                    models.PositiveIntegerField(db_column="imdb_popularity", null=True),
                ),
                ("imdb_url", models.URLField(db_column="imdb_url", null=True)),
                (
                    "rt_tomatometer_rate",
                    models.PositiveIntegerField(db_column="rt_tomatometer_rate", null=True),
                ),
                (
                    "rt_audience_rate",
                    models.PositiveIntegerField(db_column="rt_audience_rate", null=True),
                ),
                (
                    "rotten_tomatoes_url",
                    models.URLField(db_column="rotten_tomatoes_url", null=True),
                ),
                (
                    "metacritic_score",
                    models.PositiveIntegerField(db_column="metacritic_score", null=True),
                ),
                (
                    "country",
                    models.ManyToManyField(db_column="tvfy_code", to="country.country"),
                ),
                (
                    "creator",
                    models.ForeignKey(
                        db_column="creator",
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="director.director",
                    ),
                ),
                (
                    "genres",
                    models.ManyToManyField(db_column="tvfy_code", to="genre.genre"),
                ),
                (
                    "language",
                    models.ManyToManyField(db_column="tvfy_code", to="language.language"),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="SeriesCast",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "tvfy_code",
                    models.CharField(
                        db_column="tvfy_code",
                        db_index=True,
                        max_length=11,
                        unique=True,
                    ),
                ),
                (
                    "character_name",
                    models.CharField(db_column="character_name", max_length=255),
                ),
                (
                    "episode_count",
                    models.IntegerField(db_column="episode_count", null=True),
                ),
                (
                    "start_acting",
                    models.DateTimeField(db_column="start_acting", null=True),
                ),
                (
                    "end_acting",
                    models.DateTimeField(db_column="end_acting", null=True),
                ),
                (
                    "actor",
                    models.ForeignKey(
                        db_column="actor",
                        on_delete=django.db.models.deletion.CASCADE,
                        to="actor.actor",
                    ),
                ),
                (
                    "series",
                    models.ForeignKey(
                        db_column="series",
                        on_delete=django.db.models.deletion.CASCADE,
                        to="series.series",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Season",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("season", models.CharField(db_column="season", max_length=3)),
                ("imdb_url", models.URLField(db_column="imdb_url")),
                (
                    "series",
                    models.ForeignKey(
                        db_column="series",
                        on_delete=django.db.models.deletion.CASCADE,
                        to="series.series",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Episode",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "tvfy_code",
                    models.CharField(
                        db_column="tvfy_code",
                        db_index=True,
                        max_length=11,
                        unique=True,
                    ),
                ),
                ("title", models.CharField(db_column="title", max_length=255)),
                (
                    "storyline",
                    models.TextField(db_column="storyline", null=True),
                ),
                (
                    "release_date",
                    models.DateField(db_column="release_date", null=True),
                ),
                (
                    "imdb_rate",
                    models.FloatField(db_column="imdb_rate", null=True),
                ),
                (
                    "imdb_vote_count",
                    models.IntegerField(db_column="imdb_vote_count", null=True),
                ),
                (
                    "episode",
                    models.IntegerField(db_column="episode", null=True),
                ),
                (
                    "season",
                    models.ForeignKey(
                        db_column="season",
                        on_delete=django.db.models.deletion.CASCADE,
                        to="series.season",
                    ),
                ),
            ],
            options={
                "unique_together": {("episode", "season")},
            },
        ),
    ]
