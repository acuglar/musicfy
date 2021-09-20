from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.base_user import BaseUserManager
from django.db.models.manager import BaseManager


class UserManager(BaseUserManager):
    use_in_migrations = True
    
    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('The email must be set')
        
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        # user.save(using=self._db)  > settings.DATABASES - alternando db durante o proejeto
        user.save()
        
        return user
    
    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('fullname', 'NA')
        extra_fields.setdefault('is_admin', False)
        
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('fullname', 'NA')
        extra_fields.setdefault('is_admin', True)
        
        if extra_fields.get('is_admin') is not True:
            raise ValueError('Superuser must have is_admin as True')
        
        return self._create_user(email, password, **extra_fields)

        
class CustomUser(AbstractBaseUser):
    # PermissionsMixin:  definições de superuser

    email = models.EmailField(blank=False, unique=True)
    fullname = models.CharField(max_length=255)
    is_admin = models.BooleanField(default=False)

    # Removendo campos
    first_name = None
    last_name = None
    
    USERNAME_FIELD = 'email'  # ref auth user, padrão: username. VER AbstractUser
    REQUIRED_FIELDS = []
    
    objects = UserManager()  # CustomUser.objects 
