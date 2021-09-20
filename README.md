# musicfy 006_custom-user

> [Authentication](https://www.django-rest-framework.org/api-guide/authentication/#authentication)  
> [Permissions](https://www.django-rest-framework.org/api-guide/permissions/)

## extendendo comportamento de User

rel 1:1 com User na classe Artist (idealmente no início do projeto)

Redefinindo User padrão:

```py
# app.settings
AUTH_USER_MODEL = 'accounts.CustomUser''

# redefinir User para CustomUser nas views
# VER dbeaver
```

## mudando definições de user no meio do proejeto

- solução gosseira: deletar database e refazer migrations, ou;

1. deletar dados django_migrations
1. $ ./manage.py migrate --fake
1. $ ./manage.py makemigrations
1. $ ./manage.py migrate

> https://docs.djangoproject.com/en/3.2/topics/auth/customizing/#changing-to-a-custom-user-model-mid-project
