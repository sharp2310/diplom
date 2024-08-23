from django.db import models
NULLABLE = {
    'null': True,
    'blank': True,
}


class Module(models.Model):
    """Образовательный Модуль"""
    serial_number = models.AutoField(primary_key=True, verbose_name="Порядковый номер")
    title = models.CharField(max_length=150, verbose_name='Название модуля', help_text="Введите название модуля")
    description = models.TextField(verbose_name='Описание', help_text="Опишите основные материалы модуля")
    preview = models.ImageField(upload_to="modules/previews", verbose_name="Превью", **NULLABLE, help_text="Загрузите превью")
    owner = models.ForeignKey('users.User', on_delete=models.SET_NULL, verbose_name="Владелец модуля", **NULLABLE)

    last_update = models.DateField(auto_now=True, verbose_name='Последнее обновление')
    is_published = models.BooleanField(default=True, verbose_name='Опубликован')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Образовательный модуль'
        verbose_name_plural = 'Образовательные модули'
        ordering = ('serial_number',)

class Lesson(models.Model):
    module = models.ForeignKey(Module, on_delete=models.CASCADE, verbose_name='Курс', related_name='lessons')
    title = models.CharField(max_length=150, verbose_name='Название урока', help_text='Введите название урока')
    description = models.TextField(verbose_name='Описание урока', help_text='Опишите основные материалы урока')
    preview = models.ImageField(upload_to='modules/lessons/previews', verbose_name='Превью урока', **NULLABLE, help_text='Загрузите превью урока')
    video_link = models.URLField(verbose_name='Ссылка на видео', **NULLABLE, help_text='Укажите ссылку на видео урока')
    owner = models.ForeignKey('users.User',on_delete=models.SET_NULL, **NULLABLE, verbose_name='Владелец урока')
    views_count = models.PositiveIntegerField(default=0, verbose_name='Количество просмотров')


    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'

class Subscription(models.Model):
    """Подписка на Модуль"""
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, verbose_name='Пользователь')
    module = models.ForeignKey(Module, on_delete=models.CASCADE, verbose_name='модуль')

    def __str__(self):
        return f'{self.user} - {self.module}'

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        ordering = ('pk',)
        unique_together = ('user', 'module')