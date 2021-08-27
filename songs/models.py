from django.db import models


class Song(models.Model):
    """ artist 1:N songs """
    title = models.CharField(max_length=255)
    artist = models.ForeignKey("Artist", on_delete=models.CASCADE, related_name="songs")   

    def __str__(self):
        return f'{self.title}'


class Artist(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class Biography(models.Model):
    """ artist 1:1 bio """
    description = models.TextField()
    artist = models.OneToOneField(Artist, on_delete=models.CASCADE)


class Playlist(models.Model):
    """ song N:N playlist """
    title = models.CharField(max_length=255)
    songs = models.ManyToManyField(Song, related_name="playlists")