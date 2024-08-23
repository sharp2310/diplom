import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Module',
            fields=[
                ('serial_number', models.AutoField(primary_key=True, serialize=False, verbose_name='Порядковый номер')),
                ('title', models.CharField(help_text='Введите название модуля', max_length=150, verbose_name='Название модуля')),
                ('description', models.TextField(help_text='Опишите основные материалы модуля', verbose_name='Описание')),
                ('preview', models.ImageField(blank=True, help_text='Загрузите превью', null=True, upload_to='modules/previews', verbose_name='Превью')),
                ('owner', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Владелец модуля')),
            ],
            options={
                'verbose_name': 'Образовательный модуль',
                'verbose_name_plural': 'Образовательные модули',
                'ordering': ('serial_number',),
            },
        ),
    ]