import uuid

from rest_framework import serializers
from users.models import User


class UserRegisterSerializer(serializers.ModelSerializer):
    """Сериализатор для регистрации пользователя"""

    class Meta:
        model = User
        fields = ('email', 'password', 'first_name')

    def create(self, validated_data):
        """Создает нового пользователя и вызывает подтверждение регистрации"""
        user = User(
            email=validated_data['email'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            is_active=False
        )
        user.set_password(validated_data['password'])
        user.token = self.generate_token()
        user.save()
        return user

    def generate_token(self):
        """Генерирует уникальный токен для подтверждения регистрации"""
        return str(uuid.uuid4())