# Add section field to Lesson and initialize PlatformSettings

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_add_course_cover_platformsettings_news'),
    ]

    operations = [
        migrations.AddField(
            model_name='lesson',
            name='section',
            field=models.CharField(blank=True, help_text='Название раздела (например: Модуль 1, Введение)', max_length=200, verbose_name='Раздел/Модуль'),
        ),
        # Initialize PlatformSettings with default values
        migrations.RunPython(
            code=lambda apps, schema_editor: (
                apps.get_model('core', 'PlatformSettings').objects.get_or_create(
                    id=1,
                    defaults={'name': 'LMS', 'logo': ''}
                )
            ),
            reverse_code=migrations.RunPython.noop,
        ),
    ]
