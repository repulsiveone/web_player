from django.db import models
from django.contrib.auth.models import AbstractUser


class TrackList(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20, default='untitled')
    location = models.CharField(max_length=100)
    author = models.CharField(max_length=100, default='unknown')
    image = models.CharField(max_length=100, default='/static/default.jpg')

    """????"""
    objects = models.Manager()

    def __str__(self):
        return self.name


class Playlist(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    about = models.CharField(max_length=300, blank=True)
    image = models.CharField(max_length=100, default='/static/default.jpg')
    # user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    user = models.ForeignKey('player.CustomUser', on_delete=models.CASCADE)
    tracks = models.ManyToManyField(TrackList, through='PlaylistTracks')

    objects = models.Manager()

    def __str__(self):
        return self.name


class PlaylistTracks(models.Model):
    id = models.AutoField(primary_key=True)
    playlist = models.ForeignKey(Playlist, on_delete=models.CASCADE)
    track = models.ForeignKey(TrackList, on_delete=models.CASCADE)
    order_id = models.IntegerField()

    # class Meta:
    #     unique_together = ('playlist', 'track')


"""повторяется playlist придумать как правильно создать связь"""
class CustomUser(AbstractUser):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=30, unique=False)
    last_name = None
    first_name = None
    last_login = None
    date_joined = None
    email = models.EmailField(max_length=60, unique=True)
    any_playlist = models.ManyToManyField(Playlist, through='UserMusic')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    # objects = models.Manager()

    def __str__(self):
        return self.username


class UserMusic(models.Model):
    id = models.AutoField(primary_key=True)
    playlist = models.ForeignKey(Playlist, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    objects = models.Manager()


# class UserPlaylists(models.Model):
#     id = models.AutoField(primary_key=True)
#     playlist = models.ForeignKey(Playlist, on_delete=models.CASCADE)
#     user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
