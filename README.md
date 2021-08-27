# musicfy 002_models_and_relations

```sh
./manage.py makemigrations  # No changes detected
./manage.py migrate  # Apply all migrations: admin, auth, contenttypes, sessions
```

django possui estrutura padrão preconfigurada

models contém os campos e comportamentos essenciais dos dados que você está armazenando

CONVENTION: models são declaradas em singular

## criando uma model

1. Criar uma classe no arquivo models.py com o nome do objeto representado;
1. Herdar a classe models.Model;
1. Definir os campos do objeto e seus respectivos tipos, bem como algumas regras aplicadas;
1. Definir seus relacionamentos;
1. Executar a migration para que o Model seja mapeado para o banco e os dados possam ser persistidos.

fazendo as migrations:

```sh
./manage.py showmigrations
./manage.py makemigrations  # criando um script de alterações
./manage.py migrate  # persistindo alterações no bd
./manage.py showmigrations
```

## shell

```sh
./manage.py shell
```

songs > models

```py
class Song(models.Model):
    title = models.CharField(max_length=255)
    artist = models.CharField(max_length=255)
```

shell

```py
./manage.py shell
from songs.models

In [1]: from songs.models import Song

In [2]: s1 = Song.objects.create(title="Fear Of The Dark", artist="Iron Maiden")

In [3]: s2 = Song.objects.create(title="Stairway To Heaven", artist="Led Zeppelin")

In [4]: s1
Out[4]: <Song: Song object (1)>  # número refere-se ao id

In [3]: s3 = Song.objects.create(title="Wish You In Here", artist="Pynk Floid")

In [5]: s3
Out[5]: <Song: Pynk Floid - Wish You In Here>  # def __str__

# s1, s2, s3 criados em db

# OUTRA FORMA
In [6]: Song(title="Last Kiss", artist="Pearl Jam")  # sem persistência
Out[6]: <Song: Last Kiss - Pearl Jam>

In [7]: s4 = Song(title="Last Kiss", artist="Pearl Jam")  # instanciando

In [9]: s4.save()  # persistindo s4 em db
# ESSA FORMA É MAIS PERFORMATICA

# como até então não há constraint UNIQUE definida, instâncias podem ser repetidas
# Para contornar isso get_or_create():

In [10]: s5 = Song.objects.get_or_create(title="Last Kiss", artist="Pearl Jam")  # -> (objeto, bool)

In [11]: s5
Out[11]: (<Song: Last Kiss - Pearl Jam>, False)

In [12]: s6 = Song.objects.get_or_create(title="Come as You Are", artist="Nirvana")

In [13]: s6
Out[13]: (<Song: Come as You Are - Nirvana>, True)

In [14]: s7 = Song.objects.get_or_create(title="In Bloom", artist="Nirvana")
```

A criação de um artista pode ser repetida, no entanto isso implica consequências como erro de digitação. Portanto, convém dividir artist em um model própria

### Relacionamento artist 1:N song:

songs > models

```py
class Song(models.Model):
    title = models.CharField(max_length=255)
    artist = models.ForeignKey('Artist', on_delete=models.CASCADE)

class Artist(models.Model):
    name = models.CharField(max_length=255, unique=True)
```

shell

```py
In [1]: from songs.models import Song, Artist

In [2]: a1 = Artist.objects.create(name="Guns N\' Roses")

In [3]: s1 = Song.objects.create(title="Welcome To The Jungle")
IntegrityError: NOT NULL constraint failed: songs_song.artist_id
# instância de artista precisa ser passada

In [3]: s1 = Song.objects.create(title="Welcome To The Jungle", artist=a1)

In [4]: s1
Out[4]: <Song: Welcome To The Jungle>

In [5]: s1.artist
Out[5]: <Artist: Guns N Roses>

# Por padrão campos relacionados são não nulos (null=False).

# comportamentos distintos necessitam ser especificados:
# null=True,
# blank=True  > permitir campo vazio quando instanciândo e forms

# Acessando lado inverso da relação:
In [8]: a1.song_set
Out[8]: <django.db.models.fields.related_descriptors.create_reverse_many_to_one_manager.<locals>.RelatedManager at 0x7f2815f21190>

In [9]: a1.song_set.all()
Out[9]: <QuerySet [<Song: Welcome To The Jungle>]>

# default `model_set`
# add related_name='songs' songs.model.Song

In [8]: a1 = Artist.objects.get(name="Guns N' Roses")

In [9]: a1.songs.all()
Out[9]: <QuerySet [<Song: Welcome To The Jungle>]>
```

### relacionamento artist 1:1 bio

songs > models

```py
class Artist(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return f'{self.name}'

class Biography(models.Model):
    """ artist 1:1 bio """
    description = models.TextField()
    artist = models.OneToOneField(Artist, on_delete=models.CASCADE)
```

shell

```py
In [1]: from songs.models import Artist, Biography

In [3]: artist = Artist.objects.get(name="Guns N\' Roses")
# 1:1 DEFAULT null=False. artist <=> biography

# o relacionamento é bilateral, no entanto, convém racionalizar a lógica da orientação
# e.g. se biography em Artist, não poderia criar artist sem criar bio.

In [4]: b = Biography.objects.create(description="bio Guns", artist=artist)

In [5]: b
Out[5]: <Biography: Biography object (1)>

In [6]: b.artist
Out[6]: <Artist: Guns N' Roses>

In [7]: artist.biography
Out[7]: <Biography: Biography object (1)>
```

### relacionamento song N:N playlist

```py
class Song(models.Model):
    title = models.CharField(max_length=255)
    artist = models.ForeignKey('Artist', on_delete=models.CASCADE)

class Playlist(models.Model):
    title = models.CharField(max_length=255)
    songs = models.ManyToManyField(Song, related_name="playlists")
```

```py
In [1]: from songs.models import Song, Playlist

In [2]: Song.objects.all()
Out[2]: <QuerySet [<Song: Welcome To The Jungle>]>

In [3]: Song.objects.count()
Out[3]: 1

In [6]: playlist = Playlist.objects.create(title="first playlist")
# default null=True

In [7]: song = Song.objects.first()

In [8]: song
Out[8]: <Song: Welcome To The Jungle>

In [9]: playlist.songs.add(song)
# relacionando song a playlist

In [10]: playlist.songs.all()
Out[10]: <QuerySet [<Song: Welcome To The Jungle>]>

In [11]: playlist.songs.remove(song)

In [11]: playlist.songs.clear()  # removendo todos

In [12]: playlist.songs.all()
Out[12]: <QuerySet []>

In [13]: playlist.songs.add(song)

In [14]: playlist.songs.add(song)

In [15]: playlist.songs.all()
Out[15]: <QuerySet [<Song: Welcome To The Jungle>]>
# repetição não aceita

# tabela pivo para ManyToMany é criado no padrão app_tabela (songs_playlist_songs)

In [16]: song.playlist
AttributeError: 'Song' object has no attribute 'playlist'
# related_name não declarado

In [17]: song.playlist_set
Out[17]: <django.db.models.fields.related_descriptors.create_forward_many_to_many_manager.<locals>.ManyRelatedManager at 0x7fa3c32dd6a0>

# songs.models.Playlist related_name="playlists"
In [18]: song.playlists
Out[18]: <django.db.models.fields.related_descriptors.create_forward_many_to_many_manager.<locals>.ManyRelatedManager at 0x7fb2728a4ac0>
```

### instânciando muitas de uma vez

```py
In [2]: from songs.models import Artist, Song, Playlist

In [3]: artists = Artist.objects.all()

In [4]: artists
Out[4]: <QuerySet [<Artist: Guns N Roses>, <Artist: RHCP>]>

In [26]: artist = Artist.objects.first()

In [27]: song1
Out[27]: <Song: Welcome To The Jungle>

In [28]: song2 = Song.objects.create(title="November Rain", artist=artist)

In [29]: song2
Out[29]: <Song: November Rain>

In [33]: playlist.songs.clear()

In [34]: playlist.songs.add(song1, song2)
```
