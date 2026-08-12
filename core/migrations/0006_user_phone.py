# Generated migration for phone field

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_create_test_users'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='phone',
            field=models.CharField(blank=True, max_length=20, null=True, unique=True, verbose_name='Номер телефона'),
        ),
    ]
