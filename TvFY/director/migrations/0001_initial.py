# Generated by Django 4.0.4 on 2022-05-25 14:24

import django.contrib.postgres.fields
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("country", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Director",
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
                        db_column="tvfy",
                        db_index=True,
                        max_length=11,
                        unique=True,
                    ),
                ),
                (
                    "first_name",
                    models.CharField(db_column="first_name", max_length=128),
                ),
                (
                    "last_name",
                    models.CharField(db_column="last_name", max_length=128),
                ),
                (
                    "full_name",
                    models.CharField(db_column="full_name", max_length=255),
                ),
                (
                    "imdb_url",
                    models.URLField(db_column="imdb_url", null=True, unique=True),
                ),
                (
                    "rt_url",
                    models.URLField(db_column="rt_url", null=True, unique=True),
                ),
                (
                    "born_date",
                    models.DateTimeField(db_column="born_date", null=True),
                ),
                (
                    "died_date",
                    models.DateTimeField(db_column="died_date", null=True),
                ),
                (
                    "perks",
                    django.contrib.postgres.fields.ArrayField(
                        base_field=models.CharField(blank=True, db_column="perks", max_length=32),
                        null=True,
                        size=None,
                    ),
                ),
                (
                    "oscars",
                    models.PositiveSmallIntegerField(db_column="oscars", null=True),
                ),
                (
                    "oscar_nominations",
                    models.PositiveSmallIntegerField(db_column="oscar_nominations", null=True),
                ),
                (
                    "wins",
                    models.PositiveSmallIntegerField(db_column="wins", null=True),
                ),
                (
                    "nominations",
                    models.PositiveSmallIntegerField(db_column="nominations", null=True),
                ),
                (
                    "is_updated",
                    models.BooleanField(db_column="is_updated", default=False),
                ),
                (
                    "born_at",
                    models.ForeignKey(
                        db_column="born_at",
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="d_born_at",
                        to="country.country",
                    ),
                ),
                (
                    "died_at",
                    models.ForeignKey(
                        db_column="died_at",
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="d_died_at",
                        to="country.country",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
