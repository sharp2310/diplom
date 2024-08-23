from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('modules', '0003_subscription'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='lesson',
            name='is_published',
        ),
        migrations.RemoveField(
            model_name='lesson',
            name='last_update',
        ),
        migrations.AddField(
            model_name='module',
            name='is_published',
            field=models.BooleanField(default=True, verbose_name='Опубликован'),
        ),
        migrations.AddField(
            model_name='module',
            name='last_update',
            field=models.DateField(auto_now=True, verbose_name='Последнее обновление'),
        ),
    ]