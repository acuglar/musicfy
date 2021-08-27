# musicfy 001_django_introduction

## Inicializando um projeto

```sh
python3 -m venv env  # criando virtual env
source env/bin/activate  # ativando virtual env
pip install djangorestframework
django-admin startproject musicfy .  # criando projeto django
python manage.py runserver [opc port]
```

**plugins** e **apps** necessitam ter o contexto declarado em
musicfy > settings > INSTALLED_APPS

```py
INSTALLED_APPS = [
    ...,
    'rest_framework'  # renderizar templates
]

DATABASES = {...}  # default sqlite
```

## Inicializando um app

```sh
python manage.py startapp songs
touch urls.py serializers.py
```

web pages and other content are delivered by views.
views are represented by a Python function (or method).
O retorno da view corresponde a url passada em songs.urls e instanciada em musicfy.urls.

URL via outro que não GET requer slash ao final

Serializer fornece um mecanismo para formatar as models Django Normalmente, texto ou qualquer outro formato.

## ipdb

```py
ipdb> serializer
SampleSerializer(data={'name': 'Juca', 'teste': 'teste'}):
    name = CharField()
    age = IntegerField()
ipdb> request.data
{'name': 'Juca', 'teste': 'teste'}
ipdb> serializer.is_valid()
False
ipdb> serializer.data
{'name': 'Juca'}
ipdb>
```
