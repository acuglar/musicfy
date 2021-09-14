from django.db import models
from django.db.models.fields.related import ForeignKey

from accounts.models import CustomUser


class Artist(models.Model):
    name = models.CharField(max_length=255, unique=True)
    formed_in = models.IntegerField()
    status = models.CharField(max_length=255)
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, null=True)
    
    def __str__(self):
        return f'{self.name} - {self.status}'


class Song(models.Model):
    """ artist 1:N songs """
    title = models.CharField(max_length=255)
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE, related_name="songs")   

    def __str__(self):
        return self.title


class Biography(models.Model):
    """ artist 1:1 bio """
    description = models.TextField()
    artist = models.OneToOneField(Artist, on_delete=models.CASCADE)


class Playlist(models.Model):
    """ song N:N playlist """
    title = models.CharField(max_length=255)
    songs = models.ManyToManyField(Song)