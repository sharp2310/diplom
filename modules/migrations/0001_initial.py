from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Module',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('serial_number', models.PositiveIntegerField(default=0, unique=True, verbose_name='порядковый номер')),
                ('name', models.CharField(max_length=150, verbose_name='название')),
                ('description', models.TextField(default='ваше описание модуля', verbose_name='описание')),
                ('image', models.ImageField(blank=True, null=True, upload_to='modules/', verbose_name='картинка')),
                ('url_video', models.URLField(blank=True, null=True, verbose_name='ссылка на видео')),
                ('last_update', models.DateField(auto_now=True, verbose_name='последнее обновление')),
                ('is_published', models.BooleanField(default=True, verbose_name='опубликован')),
                ('views_count', models.PositiveIntegerField(default=0, verbose_name='количество просмотров')),
                ('likes', models.PositiveIntegerField(default=0, verbose_name='количество лайков')),
            ],
            options={
                'verbose_name': 'модуль',
                'verbose_name_plural': 'модули',
                'ordering': ('serial_number',),
            },
        ),
        migrations.CreateModel(
            name='Subscription',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('module', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='modules.module', verbose_name='модуль')),
            ],
            options={
                'verbose_name': 'подписка',
                'verbose_name_plural': 'подписки',
                'ordering': ('pk',),
            },
        ),
    ]