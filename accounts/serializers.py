from rest_framework import serializers


class UserSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
    is_staff = serializers.BooleanField(required=False)
    is_superuser = serializers.BooleanField(required=False)

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()


