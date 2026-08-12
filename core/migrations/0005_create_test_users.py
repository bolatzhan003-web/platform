# Generated migration to create test users

from django.db import migrations
from django.contrib.auth.hashers import make_password


def create_test_users(apps, schema_editor):
    User = apps.get_model('core', 'User')

    users_data = [
        {'username': 'admin', 'password': 'admin123', 'email': 'admin@lms.local', 'role': 'admin', 'first_name': 'Admin', 'is_staff': True, 'is_superuser': True},
        {'username': 'teacher', 'password': 'teacher123', 'email': 'teacher@lms.local', 'role': 'teacher', 'first_name': 'Teacher', 'is_staff': False},
        {'username': 'teacher2', 'password': 'teacher123', 'email': 'teacher2@lms.local', 'role': 'teacher', 'first_name': 'Teacher2', 'is_staff': False},
        {'username': 'student', 'password': 'student123', 'email': 'student@lms.local', 'role': 'student', 'first_name': 'Student', 'is_staff': False},
        {'username': 'student2', 'password': 'student123', 'email': 'student2@lms.local', 'role': 'student', 'first_name': 'Student2', 'is_staff': False},
        {'username': 'student3', 'password': 'student123', 'email': 'student3@lms.local', 'role': 'student', 'first_name': 'Student3', 'is_staff': False},
    ]

    for user_data in users_data:
        if not User.objects.filter(username=user_data['username']).exists():
            pwd = user_data.pop('password')
            user = User(**user_data)
            user.password = make_password(pwd)
            user.save()


def reverse_create_users(apps, schema_editor):
    User = apps.get_model('core', 'User')
    User.objects.filter(username__in=['admin', 'teacher', 'teacher2', 'student', 'student2', 'student3']).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_remove_video_embed_code'),
    ]

    operations = [
        migrations.RunPython(create_test_users, reverse_create_users),
    ]
