from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('modules', '0004_remove_lesson_is_published_remove_lesson_last_update_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='module',
            name='liked_users',
        ),
        migrations.RemoveField(
            model_name='module',
            name='likes',
        ),
    ]