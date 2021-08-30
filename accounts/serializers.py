from rest_framework import serializers


class UserSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True) 
    # write_only=True  > oculta password no retorno

    is_staff = serializers.BooleanField(required=False)
    is_superuser = serializers.BooleanField(required=False)

    # username e password obrigatórios
    # is_staff e is_superuser são privilégios de superuser
    # is_staff e is_superuser default=False

