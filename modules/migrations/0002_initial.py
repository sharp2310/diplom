from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('modules', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='subscription',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='пользователь'),
        ),
        migrations.AddField(
            model_name='module',
            name='liked_users',
            field=models.ManyToManyField(blank=True, related_name='liked_modules', to=settings.AUTH_USER_MODEL, verbose_name='лайкнувшие'),
        ),
        migrations.AddField(
            model_name='module',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='владелец'),
        ),
        migrations.AlterUniqueTogether(
            name='subscription',
            unique_together={('user', 'module')},
        ),
    ]