from django.db import models
from django.contrib.auth.models import AbstractUser


class TrackList(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20)
    duration = models.IntegerField()
    location = models.CharField(max_length=100)

    """????"""
    objects = models.Manager()

    def __str__(self):
        return self.name


class CustomUser(AbstractUser):
    id = models.AutoField(primary_key=True)
    last_name = None
    first_name = None
    last_login = None
    date_joined = None
    email = models.EmailField(max_length=60)
    track = models.ManyToManyField(TrackList, through='UserMusic')

    # objects = models.Manager()

    def __str__(self):
        return self.username


class UserMusic(models.Model):
    id = models.AutoField(primary_key=True)
    track = models.ForeignKey(TrackList, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    objects = models.Manager()


class Playlist(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    # user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    user = models.ForeignKey('player.CustomUser', on_delete=models.CASCADE)
    tracks = models.ManyToManyField(TrackList)

    objects = models.Manager()

    def __str__(self):
        return self.name


