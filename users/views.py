from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView
from django.urls import reverse
from config.settings import EMAIL_HOST_USER
from users.forms import UserRegisterForm, UserProfileForm, CustomSetPasswordForm
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordResetConfirmView
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from users.models import User
import uuid
from django.contrib import messages
from rest_framework import generics, status
from rest_framework.response import Response
from users.serializers import UserRegisterSerializer


class UserRegisterAPIView(generics.CreateAPIView):
    """API для регистрации нового пользователя"""
    serializer_class = UserRegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        # Генерация ссылки для подтверждения
        confirmation_link = request.build_absolute_uri(reverse('users:confirm_registration', args=[user.token]))

        # Отправка письма
        subject = 'Подтверждение регистрации'
        html_message = render_to_string('users/registration_email.html', {
            'user': user,  # Теперь user должен содержать first_name
            'confirmation_link': confirmation_link
        })
        plain_message = strip_tags(html_message)
        send_mail(subject, plain_message, EMAIL_HOST_USER, [user.email], html_message=html_message)

        return Response({'message': 'Проверьте вашу почту для подтверждения регистрации!'}, status=status.HTTP_201_CREATED)
class UserRegisterView(CreateView):
    """Регистрация нового пользователя"""
    form_class = UserRegisterForm
    template_name = 'users/user_register.html'

    def form_valid(self, form):
        """Сохранение пользователя и отправка письма для подтверждения регистрации"""
        user = form.save(commit=False)
        user.is_active = False
        user.token = self.generate_token()
        user.save()

        # Генерация ссылки для подтверждения
        confirmation_link = self.request.build_absolute_uri(reverse('users:confirm_registration', args=[user.token]))

        # Отправка письма
        subject = 'Подтверждение регистрации'
        html_message = render_to_string('users/registration_email.html', {
            'user': user,
            'confirmation_link': confirmation_link
        })
        plain_message = strip_tags(html_message)
        from_email = EMAIL_HOST_USER
        to_email = user.email
        send_mail(subject, plain_message, from_email, [to_email], html_message=html_message)

        # Показать сообщение о проверке почты
        messages.success(self.request, 'Проверьте вашу почту для подтверждения регистрации!')

        # Перенаправляем на главную страницу
        return redirect(self.get_success_url())

    def get_success_url(self):
        """Возвращает URL-адрес для перенаправления после успешной регистрации"""
        return reverse_lazy('index')

    def generate_token(self):
        """Генерирует уникальный токен для подтверждения регистрации"""
        return str(uuid.uuid4())


class UserListView(ListView):
    """View для отображения списка пользователей"""
    model = User
    template_name = 'users/user_list.html'
    context_object_name = 'users'

    def get_context_data(self, **kwargs):
        """Добавляет в контекст URL-адрес для просмотра профиля пользователя"""
        context = super().get_context_data(**kwargs)
        context['user_profile_url'] = reverse_lazy('users:user_profile')
        return context

class UserProfileView(LoginRequiredMixin, UpdateView):
    """View для отображения профиля пользователя"""

    form_class = UserProfileForm
    template_name = 'users/user_profile.html'
    success_url = reverse_lazy('users:user_profile')


    def get_object(self):
        """Возвращает текущего аутентифицированного пользователя"""
        return self.request.user


class UserProfileUpdateView(LoginRequiredMixin, UpdateView):
    """View для обновления профиля пользователя"""
    form_class = UserProfileForm
    template_name = 'users/profile_update.html'
    success_url = reverse_lazy('users:user_profile')

    def get_object(self, queryset=None):
        """Возвращает текущего аутентифицированного пользователя"""
        return self.request.user


class UserDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """View для удаления профиля пользователя"""
    model = User
    template_name = 'users/user_confirm_delete.html'
    success_url = reverse_lazy('index')

    def test_func(self):
        """Проверяет, что текущий пользователь является владельцем профиля"""
        obj = self.get_object()
        return obj == self.request.user

class UserPasswordResetView(SuccessMessageMixin, PasswordResetView):
    """View для сброса пароля пользователя"""
    template_name = 'users/password_reset.html'
    email_template_name = 'users/password_reset_email.html'
    subject_template_name = 'users/password_reset_subject.txt'
    success_message = "Ссылка для сброса пароля была отправлена на вашу почту."

    def get_success_url(self):
        """Перенаправляет на страницу входа после успешного сброса пароля"""
        return reverse_lazy('users:login')


class UserPasswordResetConfirmView(SuccessMessageMixin, PasswordResetConfirmView):
    """View для подтверждения сброса пароля"""
    template_name = 'users/password_reset_confirm.html'
    success_url = reverse_lazy('users:login')
    form_class = CustomSetPasswordForm
    success_message = "Ваш пароль успешно обновлен."

# Вход пользователя
class UserLoginView(LoginView):
    template_name = 'users/user_login.html'
    redirect_authenticated_user = True

def confirm_registration(request, token):
    try:
        user = User.objects.get(token=token)
        if user.is_active:
            messages.warning(request, "Регистрация уже подтверждена.")
            return redirect('users:login')

        # Если пользователь не активен, активируем его
        user.is_active = True
        user.token = None
        user.save()
        messages.success(request, "Ваш аккаунт успешно подтвержден! Теперь вы можете войти на сайт.")

        # Перенаправляем пользователя на его профиль после подтверждения регистрации
        return redirect('users:user_profile')

    except User.DoesNotExist:
        messages.error(request, "Неверный токен подтверждения.")
        return redirect('users:login')