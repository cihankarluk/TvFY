# Generated by Django 3.2.5 on 2021-09-10 20:48

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("actor", "0001_initial"),
        ("genre", "0002_auto_20210117_1530"),
        ("director", "0003_auto_20210909_2015"),
        ("core", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Movie",
            fields=[
                (
                    "id",
                    models.AutoField(
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
                        blank=True, db_column="updated_by", max_length=100, null=True
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
                    models.CharField(db_index=True, max_length=14, unique=True),
                ),
                ("title", models.CharField(max_length=255)),
                ("storyline", models.TextField()),
                ("release_date", models.DateField(null=True)),
                ("run_time", models.PositiveIntegerField(null=True)),
                ("rt_tomatometer_rate", models.PositiveIntegerField(null=True)),
                ("rt_audience_rate", models.PositiveIntegerField(null=True)),
                ("imdb_popularity", models.PositiveIntegerField(null=True)),
                ("imdb_rate", models.FloatField(null=True)),
                ("imdb_vote_count", models.PositiveIntegerField(null=True)),
                ("wins", models.PositiveIntegerField(default=0, null=True)),
                ("nominations", models.PositiveIntegerField(default=0, null=True)),
                ("budget", models.PositiveIntegerField(default=0, null=True)),
                ("budget_currency", models.CharField(max_length=255, null=True)),
                (
                    "usa_opening_weekend",
                    models.PositiveIntegerField(blank=True, default=0, null=True),
                ),
                (
                    "usa_opening_weekend_currency",
                    models.CharField(max_length=255, null=True),
                ),
                (
                    "ww_gross",
                    models.PositiveIntegerField(blank=True, default=0, null=True),
                ),
                ("imdb_url", models.URLField(blank=True, null=True)),
                ("rotten_tomatoes_url", models.URLField(blank=True, null=True)),
                ("country", models.ManyToManyField(to="core.Country")),
                (
                    "director",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="director.director",
                    ),
                ),
                ("genres", models.ManyToManyField(to="genre.Genre")),
                ("language", models.ManyToManyField(to="core.Language")),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="MovieCast",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("character_name", models.CharField(default="John Doe", max_length=255)),
                (
                    "actor",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="actor.actor"
                    ),
                ),
                (
                    "movie",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="movies.movie"
                    ),
                ),
            ],
        ),
    ]
