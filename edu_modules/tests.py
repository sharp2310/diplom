from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from edu_modules.models import Module
from users.models import User


class ModuleTestCase(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(email='test@test.com', password='test', is_staff=True, is_superuser=True)
        self.client.force_authenticate(user=self.user)

    def test_create_module(self):

        data = {
            "title": "test_title",
            "description": "test_description"
        }

        response = self.client.post(
            '/module/',
            data=data,
            format='json'
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )
        self.assertEqual(
            response.json(),
            {'id': 1, 'title': 'test_title', 'description': 'test_description', 'author': 1}
        )
        self.assertTrue(
            Module.objects.all().exists()
        )

    def test_list_module(self):

        module = Module.objects.create(title='test_title', description='test_description')

        response = self.client.get(
            '/module/'
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
        self.assertEqual(
            response.json()['results'],
            [{'id': module.id, 'title': 'test_title', 'description': 'test_description', 'author': None}]
        )

    def test_detail_module(self):

        module = Module.objects.create(title='test_title', description='test_description')

        response = self.client.get(
            f'/module/{module.id}/'
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
        self.assertEqual(
            response.json(),
            {'id': module.id, 'title': 'test_title', 'description': 'test_description', 'author': None}
        )

    def test_update_module(self):

        update_data = {
            "title": "test_update_title",
            "description": "test_update_description"
        }
        module = Module.objects.create(title='test_title', description='test_description')

        response = self.client.patch(
            f'/module/{module.id}/',
            data=update_data
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
        self.assertEqual(
            response.json(),
            {'id': module.id, 'title': 'test_update_title', 'description': 'test_update_description', 'author': None}
        )

    def test_destroy_lesson(self):

        module = Module.objects.create(title='test_title', description='test_description')

        response = self.client.delete(
            f'/module/{module.id}/',
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT
        )

    def tearDown(self):
        Module.objects.all().delete()
        User.objects.all().delete()