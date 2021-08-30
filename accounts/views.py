from django.contrib import auth
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import password_changed, validate_password
from django.core.exceptions import ValidationError
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token

from accounts.serializers import UserSerializer


class UserView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)

        if not serializer.is_valid():
            Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(username=serializer.validated_data['username']).exists():
            # django.contrib.auth.models.User  > model auth precadastrada django
            return Response({'error': 'username already exists'}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

        # user = User.objects.create(**serializer.validated_data)  > NÃO GERA HASH DA SENHA
        # user = User.objects.create_user(**serializer.validated_data)  > CHAMA HASH ANTES DE SALVAR
        # user = User.objects.create_superuser(**serializer.validated_data)
        user = User(username=serializer.validated_data['username'])

        password = serializer.validated_data['password']

        try:
            validate_password(password, user)
            # "password_too_short": "This password is too short. It must contain at least 8 characters.",
            # "password_too_common": "This password is too common.",
            # "password_entirely_numeric": "This password is entirely numeric."
        except ValidationError as e:
            errors = {}

            for arg in e.args[0]:
                errors[arg.code] = arg.messages[0]
                
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(password)
        # NOT user.password = password

        user.save()
        # user = User.objects.create_user(**serializer.validated_data)
        
        serializer = UserSerializer(user)
        
        return Response(serializer.data)


class LoginView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        user = authenticate(**serializer.validated_data)
        # authenticate verifica se a senha informada confere e retorna instância or None
        
        if user:
            token = Token.objects.get_or_create(user=user)[0]
            return Response({'token': token.key})
        else:
            return Response({'Unauthorized': 'Failed to authenticate'}, status=status.HTTP_401_UNAUTHORIZED)
