from django.test import TestCase
from rest_framework import serializers

from users.models import User
from users.serializers import UserSerializer, UserRegisterSerializer


class TestUserSerializers(TestCase):

    def test_user_register_serializer(self):
        user_data = {
            'email': 'test@example.com',
            'password': 'testpass',
            'password2': 'testpass',
            'name': 'Test User'
        }

        serializer = UserRegisterSerializer(data=user_data)
        self.assertTrue(serializer.is_valid())

        user = serializer.save()
        self.assertEqual(user.email, user_data['email'])
        self.assertEqual(user.name, user_data['name'])

    def test_user_register_serializer_invalid_passwords(self):
        user_data = {
            'email': 'test@example.com',
            'password': 'testpass',
            'password2': 'invalidpass',
            'name': 'Test User'
        }

        serializer = UserRegisterSerializer(data=user_data)
        self.assertTrue(serializer.is_valid())

        with self.assertRaises(serializers.ValidationError):
            user = serializer.save()

    def test_user_serializer(self):
        user = User.objects.create(email='test@example.com', name='Test User')
        serializer = UserSerializer(instance=user)
        data = serializer.data
        self.assertEqual(data['email'], 'test@example.com')
        self.assertEqual(data['name'], 'Test User')