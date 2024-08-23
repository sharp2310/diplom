from rest_framework.test import APIClient, APITestCase
from rest_framework import status
from django.urls import reverse
from users.models import User
from modules.models import Module, Lesson, Subscription

class ModuleAPITestCase(APITestCase):

    @classmethod
    def setUpTestData(cls):
        # Создаем пользователей
        cls.user = User.objects.create_user(email='user@educate.com', password='password', is_active=True)

        # Создаем администратора
        cls.admin_user = User.objects.create_superuser(email='admin@educate.com', password='adminpassword')

        # Создаем клиент для тестирования
        cls.client = APIClient()

        # Создаем модуль, владельцем которого является обычный пользователь
        cls.module = Module.objects.create(
            title='Test Module',
            description='Original description',
            owner=cls.user
        )

    def test_module_update_by_owner(self):
        """Тест обновления модуля пользователем-владельцем"""
        self.client.force_authenticate(user=self.user)  # Аутентификация пользователя
        url = reverse('modules:module_update', kwargs={'pk': self.module.pk})

        new_data = {'description': 'Updated description'}
        response = self.client.patch(url, data=new_data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)  # Проверка статуса
        self.module.refresh_from_db()  # Обновление данных модуля из базы данных
        self.assertEqual(self.module.description, 'Updated description')  # Проверка обновленного значения

    def test_module_update_by_admin(self):
        """Тест обновления модуля администратором"""
        self.client.force_authenticate(user=self.admin_user)  # Аутентификация администратора
        url = reverse('modules:module_update', kwargs={'pk': self.module.pk})

        new_data = {'description': 'Admin updated description'}
        response = self.client.patch(url, data=new_data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)  # Проверка статуса
        self.module.refresh_from_db()  # Обновление данных модуля из базы данных
        self.assertEqual(self.module.description, 'Admin updated description')  # Проверка обновленного значения

    def test_module_update_by_unauthorized_user(self):
        """Тест обновления модуля неавторизованным пользователем"""
        unauthenticated_user = User.objects.create_user(email='unauth@educate.com', password='password', is_active=True)
        self.client.force_authenticate(user=unauthenticated_user)  # Аутентификация не владельцем
        url = reverse('modules:module_update', kwargs={'pk': self.module.pk})

        new_data = {'description': 'Unauthorized update'}
        response = self.client.patch(url, data=new_data)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_module_update_without_authentication(self):
        """Тест обновления модуля без аутентификации"""
        url = reverse('modules:module_update', kwargs={'pk': self.module.pk})

        new_data = {'description': 'No auth update'}
        response = self.client.patch(url, data=new_data)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

class LessonAPITestCase(APITestCase):

    @classmethod
    def setUpTestData(cls):
        # Создание администратора
        cls.admin_user = User.objects.create_user(email='admin@educate.com', password='password')
        # Создание обычного пользователя
        cls.regular_user = User.objects.create_user(email='user@educate.com', password='password')
        # Создание модуля, который будет использоваться в тестах
        cls.module = Module.objects.create(title='Test Module', owner=cls.admin_user)

    def test_lesson_create_by_admin(self):
        """Тест создания урока администратором"""
        self.client.force_authenticate(user=self.admin_user)
        url = reverse('modules:lesson_create')
        new_data = {
            'title': 'New Lesson Title',
            'description': 'Admin created lesson',
            'module': self.module.pk,
            'video_link': 'http://www.youtube.com/video.mp4',
        }
        response = self.client.post(url, new_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_lesson_update_by_admin(self):
        """Тест редактирования урока администратором"""
        self.client.force_authenticate(user=self.admin_user)
        lesson = Lesson.objects.create(
            title='Original Lesson',
            description='Original description',
            module=self.module,
            video_link='http://www.youtube.com/original_video.mp4',
            owner=self.admin_user
        )
        url = reverse('modules:lesson_update', args=[lesson.pk])
        updated_data = {
            'title': 'Updated Lesson Title',
            'description': 'Updated description',
            'module': self.module.pk,
            'video_link': 'http://www.youtube.com/updated_video.mp4',
        }
        response = self.client.put(url, updated_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        lesson.refresh_from_db()
        self.assertEqual(lesson.title, 'Updated Lesson Title')
        self.assertEqual(lesson.description, 'Updated description')

    def test_lesson_delete_by_admin(self):
        """Тест удаления урока администратором"""
        self.client.force_authenticate(user=self.admin_user)
        lesson = Lesson.objects.create(
            title='Lesson to be deleted',
            description='This lesson will be deleted.',
            module=self.module,
            video_link='http://www.youtube.com/video_to_delete.mp4',
            owner=self.admin_user
        )
        url = reverse('modules:lesson_delete', args=[lesson.pk])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        with self.assertRaises(Lesson.DoesNotExist):
            lesson.refresh_from_db()

    def test_lesson_update_by_user(self):
        """Тест редактирования урока пользователем"""
        self.client.force_authenticate(user=self.regular_user)
        # Создаем урок, который будет редактироваться
        lesson = Lesson.objects.create(
            title='Lesson to be updated',
            description='This lesson will be updated.',
            module=self.module,
            video_link='http://www.youtube.com/lesson_to_be_updated.mp4',
            owner=self.admin_user  # Урок принадлежит администратору
        )
        url = reverse('modules:lesson_update', args=[lesson.pk])  # URL для обновления
        updated_data = {
            'title': 'Updated Lesson Title by User',
            'description': 'Updated description by user',
            'module': self.module.pk,
            'video_link': 'http://www.youtube.com/updated_video_by_user.mp4',
        }
        response = self.client.put(url, updated_data)
        # Проверка на неудачное обновление, так как пользователь не является владельцем
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_lesson_delete_by_user(self):
        """Тест удаления урока пользователем"""
        self.client.force_authenticate(user=self.regular_user)
        # Создаем урок, который будет удаляться
        lesson = Lesson.objects.create(
            title='Lesson to be deleted',
            description='This lesson will be deleted.',
            module=self.module,
            video_link='http://www.youtube.com/video_to_delete.mp4',
            owner=self.admin_user  # Урок принадлежит администратору
        )
        url = reverse('modules:lesson_delete', args=[lesson.pk])
        response = self.client.delete(url)
        # Проверка на неудачное удаление, так как пользователь не является владельцем
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class SubscriptionAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(email='admin@educate.ru')
        self.user.set_password('adminpassword')
        self.user.is_superuser = True
        self.user.is_staff = True
        self.user.save()
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.module = Module.objects.create(title="Робототехника для детей")

    def test_subscribe(self):
        url = reverse('modules:module_subscription', args=[self.module.pk])
        data = {
            "module": self.module.pk
        }
        response = self.client.post(url, data=data)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Обновлено сообщение
        self.assertEqual(data, {'message': 'Подписка оформлена'})

    def test_unsubscribe(self):
        url = reverse('modules:module_subscription', args=[self.module.pk])
        data = {
            "module": self.module.pk
        }
        Subscription.objects.create(module=self.module, user=self.user)
        response = self.client.post(url, data=data)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Обновлено сообщение
        self.assertEqual(data, {'message': 'Подписка отменена'})