#!/usr/bin/env python
"""Создание тестовых пользователей для LMS."""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lms.settings')
django.setup()

from core.models import User, Course

# Удалим старых пользователей если они есть
User.objects.all().delete()

# Создаём пользователей
users = [
    {'username': 'admin', 'password': 'admin123', 'email': 'admin@lms.local', 'role': 'admin', 'first_name': 'Admin'},
    {'username': 'teacher', 'password': 'teacher123', 'email': 'teacher@lms.local', 'role': 'teacher', 'first_name': 'Teacher'},
    {'username': 'teacher2', 'password': 'teacher123', 'email': 'teacher2@lms.local', 'role': 'teacher', 'first_name': 'Teacher2'},
    {'username': 'student', 'password': 'student123', 'email': 'student@lms.local', 'role': 'student', 'first_name': 'Student'},
    {'username': 'student2', 'password': 'student123', 'email': 'student2@lms.local', 'role': 'student', 'first_name': 'Student2'},
    {'username': 'student3', 'password': 'student123', 'email': 'student3@lms.local', 'role': 'student', 'first_name': 'Student3'},
]

for user_data in users:
    pwd = user_data.pop('password')
    user = User.objects.create_user(**user_data)
    user.set_password(pwd)
    if user_data['role'] == 'admin':
        user.is_staff = True
        user.is_superuser = True
    user.save()
    print(f'✓ Created: {user.username} ({user.role})')

print('\n✅ All users created!')
print('\nTest accounts:')
print('admin / admin123')
print('teacher / teacher123')
print('student / student123')
