# Generated by Django 3.1.2 on 2021-02-20 16:05

from django.db import migrations, models

import TvFY.core.helpers


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Account",
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
                ("password", models.CharField(max_length=128, verbose_name="password")),
                (
                    "last_login",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="last login"
                    ),
                ),
                (
                    "username",
                    models.CharField(
                        max_length=50,
                        unique=True,
                        validators=[TvFY.core.helpers.UnicodeUsernameValidator()],
                    ),
                ),
                ("email", models.CharField(max_length=100)),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
