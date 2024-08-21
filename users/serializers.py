from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from users.models import User


class UserSerializer(serializers.ModelSerializer):
    """User serializer"""

    class Meta:
        model = User
        fields = "__all__"


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token["email"] = user.email
        return token