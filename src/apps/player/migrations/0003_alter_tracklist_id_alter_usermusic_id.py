# Generated by Django 4.2 on 2023-05-01 09:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('player', '0002_rename_localion_tracklist_location'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tracklist',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='usermusic',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
