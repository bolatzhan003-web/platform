# Generated migration for platform settings, course cover, and news

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_user_phone'),
    ]

    operations = [
        migrations.CreateModel(
            name='PlatformSettings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='LMS', max_length=200, verbose_name='Название платформы')),
                ('logo', models.ImageField(blank=True, null=True, upload_to='platform/', verbose_name='Логотип')),
            ],
            options={
                'verbose_name': 'Настройки платформы',
                'verbose_name_plural': 'Настройки платформы',
            },
        ),
        migrations.CreateModel(
            name='News',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='Название новости')),
                ('image', models.ImageField(upload_to='news/', verbose_name='Изображение')),
                ('description', models.TextField(verbose_name='Описание')),
                ('link', models.URLField(blank=True, null=True, verbose_name='Ссылка (опционально)')),
                ('link_text', models.CharField(blank=True, default='Подробнее', max_length=100, verbose_name='Текст кнопки')),
                ('is_active', models.BooleanField(default=True, verbose_name='Активна')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('order', models.PositiveIntegerField(default=0, verbose_name='Порядок')),
            ],
            options={
                'verbose_name': 'Новость',
                'verbose_name_plural': 'Новости',
                'ordering': ['-order', '-created_at'],
            },
        ),
        migrations.AddField(
            model_name='course',
            name='cover',
            field=models.ImageField(blank=True, null=True, upload_to='courses/', verbose_name='Обложка курса'),
        ),
    ]
