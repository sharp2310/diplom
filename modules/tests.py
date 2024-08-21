from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from modules.models import Module
from users.models import User


# Create your tests here.
class ModuleTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(email="helen597@yandex.ru")
        self.user.set_password("59hl71ee")
        self.client.force_authenticate(user=self.user)
        self.module = Module.objects.create(
            title="Module 1. Introduction",
            description="Введение",
            owner=self.user
        )

    def test_module_create(self):
        """Test module creation"""
        url = reverse("modules:module-list")
        data = {
            "title": "Module 2. Basics",
            "description": "Основы",
            "owner": self.user.pk,
        }
        response = self.client.post(url, data)
        print("\ntest_module_create")
        print(response.json())
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Module.objects.all().count(), 2)

    def test_module_retrieve(self):
        """Test module detail view"""
        url = reverse("modules:module-detail", args=(self.module.pk,))
        response = self.client.get(url)
        print("\ntest_module_retrieve")
        data = response.json()
        print(data)
        print(self.module)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("title"), self.module.title)

    def test_module_update(self):
        """Test module update"""
        url = reverse("modules:module-detail", args=(self.module.pk,))
        data = {"title": "Module 1. Present Simple"}
        response = self.client.patch(url, data)
        data = response.json()
        print("\ntest_module_update")
        print(response.json())
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("title"), "Module 1. Present Simple")

    def test_module_delete(self):
        """Test module delete"""
        url = reverse("modules:module-detail", args=(self.module.pk,))
        # self.module.owner = self.user
        response = self.client.delete(url)
        print("\ntest_module_delete")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Module.objects.all().count(), 0)

    def test_module_list(self):
        """Test module list view"""
        url = reverse("modules:module-list")
        response = self.client.get(url)
        print("\ntest_module_list")
        print(response.json())
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Module.objects.all().count(), 1)