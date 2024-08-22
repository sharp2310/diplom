from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from .managers import CustomUserManager

NULLABLE = {'blank': True, 'null': True}


class User(AbstractUser):
    """
    Модель пользователя сервисом.
    """
    username = None

    email = models.EmailField(_("email address"), unique=True)
    phone = models.CharField(max_length=35, verbose_name='Телефон', **NULLABLE)
    telegram_id = models.CharField(max_length=50, verbose_name='телеграм_ID', **NULLABLE)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'