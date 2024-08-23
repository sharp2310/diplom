import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('modules', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='module',
            name='liked_users',
            field=models.ManyToManyField(blank=True, related_name='liked_modules', to=settings.AUTH_USER_MODEL, verbose_name='лайкнувшие'),
        ),
        migrations.AddField(
            model_name='module',
            name='likes',
            field=models.PositiveIntegerField(default=0, verbose_name='Количество лайков'),
        ),
        migrations.CreateModel(
            name='Lesson',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(help_text='Введите название урока', max_length=150, verbose_name='Название урока')),
                ('description', models.TextField(help_text='Опишите основные материалы урока', verbose_name='Описание урока')),
                ('preview', models.ImageField(blank=True, help_text='Загрузите превью урока', null=True, upload_to='modules/lessons/previews', verbose_name='Превью урока')),
                ('video_link', models.URLField(blank=True, help_text='Укажите ссылку на видео урока', null=True, verbose_name='Ссылка на видео')),
                ('last_update', models.DateField(auto_now=True, verbose_name='Последнее обновление')),
                ('is_published', models.BooleanField(default=True, verbose_name='Опубликован')),
                ('views_count', models.PositiveIntegerField(default=0, verbose_name='Количество просмотров')),
                ('module', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lessons', to='modules.module', verbose_name='Курс')),
                ('owner', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Владелец урока')),
            ],
            options={
                'verbose_name': 'Урок',
                'verbose_name_plural': 'Уроки',
            },
        ),
    ]