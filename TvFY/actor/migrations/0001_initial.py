# Generated by Django 3.1.2 on 2021-02-17 19:52

import django.contrib.postgres.fields
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("core", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Actor",
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
                ("first_name", models.CharField(max_length=128)),
                ("last_name", models.CharField(max_length=128)),
                ("imdb_url", models.URLField(blank=True, null=True, unique=True)),
                ("born_date", models.DateField(null=True)),
                ("died_date", models.DateField(null=True)),
                (
                    "perks",
                    django.contrib.postgres.fields.ArrayField(
                        base_field=models.CharField(blank=True, max_length=32),
                        null=True,
                        size=None,
                    ),
                ),
                ("oscars", models.PositiveSmallIntegerField(default=0)),
                ("oscar_nominations", models.PositiveSmallIntegerField(default=0)),
                (
                    "wins",
                    models.PositiveSmallIntegerField(blank=True, default=0, null=True),
                ),
                (
                    "nominations",
                    models.PositiveSmallIntegerField(blank=True, default=0, null=True),
                ),
                (
                    "born_at",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="actor_born_at",
                        to="core.country",
                    ),
                ),
                (
                    "died_at",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="actor_died_at",
                        to="core.country",
                    ),
                ),
            ],
        ),
    ]
