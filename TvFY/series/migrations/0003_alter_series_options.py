# Generated by Django 3.2.5 on 2021-07-30 19:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('series', '0002_auto_20210221_1320'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='series',
            options={'ordering': ('id',)},
        ),
    ]