# musicfy 005_authentication

> [Authentication](https://www.django-rest-framework.org/api-guide/authentication/#authentication) > [Permissions](https://www.django-rest-framework.org/api-guide/permissions/)

1. Criando app accounts:

```sh
./manage.py startapp accounts
```

2. musicfy.settings

```py
INSTALLED_APPS = [
    ...,
    'rest_framework.authtoken',  # login
    'accounts',
]
```

3. migrações de rest_framework.authtoken:

```sh
./manage.py migrate
```

4. accounts.serializers.UserSerializer
1. accounts.views.UserView
1. accounts.views.LoginView

1. musicfy.urls

NOTA: autenticação por si não permite ou nega acesso ao sistema, ela simplesmente identifica as credenciais com as quais a solicitação foi feita.

# routes

Accounts

```
POST Register
{
	"username": username,
	"password": password,
	"is_staff": is_staff,  # required=False
	"is_superuser": is_superuser  # required=False
}
```

```
POST Login
{
	"username": username,
	"password": password
}
```

# configurando autenticação

Insomnia.Accounts.Login

```
200, {"token": "aeba24253931e66786ce18e950048bc73ad9055c"}
```

Insomnia.Artists.POSTCreateArtist.Header  
Insomnia.Artists.GETListArtists.Header

```
Authorization Token aeba24253931e66786ce18e950048bc73ad9055c
```

songs.views.Artist

```py
from rest_framework.authentication import TokenAuthentication, BasicAuthentication

class ArtistView
    authentication_classes = [TokenAuthentication, BasicAuthentication]
    ...
```

# permissões de acesso a rota

songs.views.Artist

```py
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAdminUser

class ArtistView
    permission_classes = [IsAuthenticatedOrReadOnly | IsAdminUser]
    ...
```

Token padrão django não expira
Usar JOSON Web Token Authentiation

# ipdb

songs.views.Artist

```py
dir(request)
request.user
request.user.is_staff
request.user.is_superuser
```
