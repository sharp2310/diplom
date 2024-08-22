from django.conf import settings
from django.db import models

from users.models import NULLABLE


class Module(models.Model):
    """ Модель - Образовательные модули """

    title = models.CharField(max_length=255, verbose_name='Название модуля')
    description = models.TextField(**NULLABLE, verbose_name='Описание модуля')

    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                               **NULLABLE, related_name='authored_modules', verbose_name='Автор')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Модуль'
        verbose_name_plural = 'Модули'