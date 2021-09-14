from django.contrib import auth
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token

from accounts.serializers import UserSerializer, LoginSerializer
from accounts.models import CustomUser

class UserView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        if CustomUser.objects.filter(email=serializer.validated_data['email']).exists():
            return Response({'error': 'email already exists'}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

        user = CustomUser.objects.create_user(**serializer.validated_data)
        
        serializer = UserSerializer(user)
        
        return Response(serializer.data)



class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        user = authenticate(**serializer.validated_data)
      
        if user:
            token = Token.objects.get_or_create(user=user)[0]
            return Response({'token': token.key})
        else:
            return Response({'Unauthorized': 'Failed to authenticate'}, status=status.HTTP_401_UNAUTHORIZED)
