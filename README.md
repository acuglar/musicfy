# musicfy 003_serializers

serialização: instâncias de models para JSON  
desserialização: payload JSON para instânciar models

## [serializer fields](https://www.django-rest-framework.org/api-guide/fields/)

## shell

salvando no bd muitos objetos de uma vez:

```py
In [1]: from songs.models import Artist, Song

In [2]: artists = Artist.objects.bulk_create([
   ...:     Artist(name="Dio"),
   ...:     Artist(name="Black Sabbath"),
   ...:     Artist(name="Pink Floyd"),
   ...:     ])
# save() included in context bulk_create()

In [3]: artists
Out[3]: [<Artist: Dio>, <Artist: Black Sabbath>, <Artist: Pink Floyd>]

In [4]: a1 = artists[0]

In [5]: a2 = artists[1]

In [6]: a3 = artists[2]

In [7]: songs = Song.objects.bulk_create([
    ...:     Song(title="Holy Diver", artist=a1),
    ...:     Song(title="Rainbow In The Dark", artist=a1),
    ...:     Song(title="A National Acrobat", artist=a2),
    ...:     Song(title="Paranoid", artist=a2),
    ...:     Song(title="Children Of The Grave", artist=a2),
    ...:     Song(title="Shine On You Crazy Diamond", artist=a3),
    ...:     ])
```
