from django.db import models


class Artist(models.Model):
    name = models.CharField(max_length=255, unique=True)
    formed_in = models.IntegerField(default=2021)
    status = models.CharField(default='Active', max_length=255)
    
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
    songs = models.ManyToManyField(Song, related_name="playlists")