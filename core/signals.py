"""
Инициализация пользователей при первом запуске приложения.
Запускается автоматически из settings.py
"""
from django.core.management import call_command
from django.db.models.signals import post_migrate
from django.dispatch import receiver

from .models import User


@receiver(post_migrate)
def create_default_users(sender, **kwargs):
    """Создаёт тестовых пользователей после миграций."""
    if sender.name != 'core':
        return

    users_to_create = [
        {
            'username': 'admin',
            'email': 'admin@lms.local',
            'password': 'admin123',
            'first_name': 'Admin',
            'role': 'admin',
            'is_staff': True,
            'is_superuser': True,
        },
        {
            'username': 'teacher',
            'email': 'teacher@lms.local',
            'password': 'teacher123',
            'first_name': 'Teacher',
            'role': 'teacher',
        },
        {
            'username': 'teacher2',
            'email': 'teacher2@lms.local',
            'password': 'teacher123',
            'first_name': 'Teacher2',
            'role': 'teacher',
        },
        {
            'username': 'student',
            'email': 'student@lms.local',
            'password': 'student123',
            'first_name': 'Student',
            'role': 'student',
        },
        {
            'username': 'student2',
            'email': 'student2@lms.local',
            'password': 'student123',
            'first_name': 'Student2',
            'role': 'student',
        },
        {
            'username': 'student3',
            'email': 'student3@lms.local',
            'password': 'student123',
            'first_name': 'Student3',
            'role': 'student',
        },
    ]

    for user_data in users_to_create:
        username = user_data['username']
        if not User.objects.filter(username=username).exists():
            password = user_data.pop('password')
            user = User.objects.create_user(**user_data)
            user.set_password(password)
            user.save()
            print(f'✓ Created user: {username}')
