from django.test import TestCase
from users.models import User
from users.forms import UserRegisterForm, UserProfileForm, CustomSetPasswordForm, CustomPasswordResetForm
from django.urls import reverse
from django.contrib.messages import get_messages


class CustomUserManagerTests(TestCase):
    def setUp(self):
        self.email = 'test@educate.com'
        self.password = 'testpassword'

    def test_create_user(self):
        user = User.objects.create_user(email=self.email, password=self.password)
        self.assertEqual(user.email, self.email)
        self.assertTrue(user.check_password(self.password))
        self.assertFalse(user.is_superuser)

    def test_create_user_without_email(self):
        with self.assertRaises(ValueError):
            User.objects.create_user(email='', password=self.password)

    def test_create_superuser(self):
        superuser = User.objects.create_superuser(email=self.email, password=self.password)
        self.assertEqual(superuser.email, self.email)
        self.assertTrue(superuser.is_superuser)
        self.assertTrue(superuser.is_staff)

    def test_create_superuser_without_is_staff(self):
        with self.assertRaises(ValueError):
            User.objects.create_superuser(email=self.email, password=self.password, is_staff=False)

    def test_create_superuser_without_is_superuser(self):
        with self.assertRaises(ValueError):
            User.objects.create_superuser(email=self.email, password=self.password, is_superuser=False)


class UserRegisterFormTests(TestCase):
    def setUp(self):
        self.valid_data = {
            'email': 'test@educate.com',
            'first_name': 'Test',
            'last_name': 'User',
            'password1': 'testpassword',
            'password2': 'testpassword',
        }

    def test_form_valid(self):
        form = UserRegisterForm(data=self.valid_data)
        self.assertTrue(form.is_valid())
        user = form.save(commit=False)
        self.assertIsNone(user.pk)
        form.save()
        self.assertIsNotNone(user.pk)

    def test_password_mismatch(self):
        invalid_data = self.valid_data.copy()
        invalid_data['password2'] = 'differentpassword'
        form = UserRegisterForm(data=invalid_data)
        self.assertFalse(form.is_valid())
        self.assertIn('password2', form.errors)

    def test_save_hast_password(self):
        form = UserRegisterForm(data=self.valid_data)
        user = form.save()
        self.assertTrue(user.check_password(self.valid_data['password1']))


class UserProfileFormTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='test@educate.com', password='testpassword')
        self.valid_data = {
            'email': 'update@educate.com',
            'first_name': 'Updated',
            'last_name': 'Name',
        }

    def test_form_valid(self):
        form = UserProfileForm(instance=self.user, data=self.valid_data)
        self.assertTrue(form.is_valid())
        profile = form.save()
        self.assertEqual(profile.email, self.valid_data['email'])


class CustomSetPasswordFormTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='test@educate.com', password='testpassword')
        self.new_password_data = {
            'new_password1': '789test123',
            'new_password2': '789test123',
        }

    def test_set_password(self):
        form = CustomSetPasswordForm(user=self.user, data=self.new_password_data)
        self.assertTrue(form.is_valid())
        user = form.save()
        self.assertTrue(user.check_password(self.new_password_data['new_password1']))

class CustomPasswordResetFormTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='test@educate.com', password='testpassword')

    def test_clean_email_existing_user(self):
        form = CustomPasswordResetForm(data={'email': 'test@educate.com'})
        self.assertTrue(form.is_valid())

    def test_clean_email_non_existing_user(self):
        form = CustomPasswordResetForm(data={'email': 'notexisting@educate.com'})
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)

class UserViewsTests(TestCase):
    def setUp(self):
        # Создаем тестового пользователя
        self.user = User.objects.create_user(
            email='test@educate.com',
            password='testpassword',
            first_name='Test',
            last_name='User',
            is_active=True,
            telegram='test_telegram'
        )
        self.client.login(email='test@educate.com', password='testpassword')

    def test_user_register_view(self):
        response = self.client.post(reverse('users:register'), {
            'email': 'newuser@educate.com',
            'first_name': 'New',
            'last_name': 'User',
            'password1': 'testpassword',
            'password2': 'testpassword',
            'telegram': 'new_telegram'
        })
        # Проверьте, что редирект произошел
        self.assertRedirects(response, reverse('index'))

        # Проверка наличия сообщения о подтверждении
        messages = list(get_messages(response.wsgi_request))  # Получаем сообщения
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]),
                         'Проверьте вашу почту для подтверждения регистрации!')

    def test_user_list_view(self):
        response = self.client.get(reverse('users:user_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/user_list.html')
        self.assertIn(self.user, response.context['users'])

    def test_user_profile_view(self):
        response = self.client.get(reverse('users:user_profile'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/user_profile.html')
        self.assertEqual(response.context['form'].instance, self.user)

    def test_user_profile_update_view(self):
        response = self.client.post(reverse('users:profile_update'), {
            'email': 'updated@educate.com',
            'first_name': 'Updated',
            'last_name': 'User',
            'telegram': 'updated_telegram'
        })
        self.user.refresh_from_db()
        self.assertRedirects(response, reverse('users:user_profile'))
        self.assertEqual(self.user.email, 'updated@educate.com')


    def test_user_delete_view(self):
        response = self.client.post(reverse('users:user_delete', args=[self.user.pk]))
        self.assertRedirects(response, reverse('index'))
        self.assertFalse(User.objects.filter(pk=self.user.pk).exists())