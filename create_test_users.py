#!/usr/bin/env python
"""Create test users for LMS."""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lms.settings')
django.setup()

from core.models import User

# Delete existing test users
User.objects.filter(username__in=['admin', 'teacher', 'teacher2', 'student', 'student2', 'student3']).delete()

# Create users
users = [
    {'username': 'admin', 'password': 'admin123', 'email': 'admin@lms.local', 'role': 'admin', 'first_name': 'Admin', 'is_staff': True, 'is_superuser': True},
    {'username': 'teacher', 'password': 'teacher123', 'email': 'teacher@lms.local', 'role': 'teacher', 'first_name': 'Teacher'},
    {'username': 'teacher2', 'password': 'teacher123', 'email': 'teacher2@lms.local', 'role': 'teacher', 'first_name': 'Teacher2'},
    {'username': 'student', 'password': 'student123', 'email': 'student@lms.local', 'role': 'student', 'first_name': 'Student'},
    {'username': 'student2', 'password': 'student123', 'email': 'student2@lms.local', 'role': 'student', 'first_name': 'Student2'},
    {'username': 'student3', 'password': 'student123', 'email': 'student3@lms.local', 'role': 'student', 'first_name': 'Student3'},
]

for user_data in users:
    pwd = user_data.pop('password')
    is_staff = user_data.pop('is_staff', False)
    is_superuser = user_data.pop('is_superuser', False)

    user = User.objects.create_user(**user_data)
    user.set_password(pwd)
    user.is_staff = is_staff
    user.is_superuser = is_superuser
    user.save()
    print(f'✓ Created: {user.username} ({user.role}) - password: {pwd}')

print('\n✅ All users created!')
print('\n📋 Test Accounts:')
print('admin / admin123 (Администратор)')
print('teacher / teacher123 (Учитель)')
print('teacher2 / teacher123 (Учитель 2)')
print('student / student123 (Ученик)')
print('student2 / student123 (Ученик 2)')
print('student3 / student123 (Ученик 3)')
