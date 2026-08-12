# Add avatar field to User

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_add_lesson_section_init_platformsettings'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='avatar',
            field=models.ImageField(blank=True, null=True, upload_to='avatars/', verbose_name='Фото профиля'),
        ),
    ]
