# Generated by Django 3.1.2 on 2021-01-17 15:30
import json
import os

from django.db import migrations

from TvFY.genre.models import Genre


def get_response():
    dir_path = os.getcwd()
    with open(os.path.join(dir_path, 'fixtures/genre/genres.json')) as f:
        return f.read()


def create_genre_data(apps, schema_editor):
    file = json.loads(get_response())
    for data in file:
        Genre.objects.create(**data["fields"])


class Migration(migrations.Migration):
    dependencies = [
        ('genre', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_genre_data)
    ]
