# Generated by Django 3.1.2 on 2020-11-02 18:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('series', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Episode',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('imdb_rate', models.FloatField(blank=True, null=True)),
                ('release_date', models.DateField()),
                ('storyline', models.TextField()),
            ],
        ),
    ]
