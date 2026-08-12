import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lms.settings')
django.setup()

from django.contrib.auth import get_user_model
from core.models import Course, Lesson, ClassGroup

User = get_user_model()

print('Setting up local development database...\n')

# 1. Создаём пользователей если их нет
print('1. Creating users...')

admin, created = User.objects.get_or_create(
    username='admin',
    defaults={
        'email': 'admin@lms.local',
        'first_name': 'Admin',
        'last_name': 'User',
        'role': 'admin',
        'is_staff': True,
        'is_superuser': True,
    }
)
if created:
    admin.set_password('admin123')
    admin.save()
    print('  + Admin created: admin / admin123')
else:
    print('  - Admin exists')

teacher, created = User.objects.get_or_create(
    username='teacher',
    defaults={
        'email': 'teacher@lms.local',
        'first_name': 'Ivan',
        'last_name': 'Petrov',
        'role': 'teacher',
        'is_staff': True,
    }
)
if created:
    teacher.set_password('teacher123')
    teacher.save()
    print('  + Teacher created: teacher / teacher123')
else:
    print('  - Teacher exists')

student, created = User.objects.get_or_create(
    username='student',
    defaults={
        'email': 'student@lms.local',
        'first_name': 'Aliya',
        'last_name': 'Nurlanova',
        'role': 'student',
    }
)
if created:
    student.set_password('student123')
    student.save()
    print('  + Student created: student / student123')
else:
    print('  - Student exists')

# 2. Создаём курс
print('\n2. Creating course...')
course, created = Course.objects.get_or_create(
    title='Python Programming Basics',
    defaults={
        'description': 'Learn Python from scratch with video lessons and practice materials.',
        'author': teacher,
    }
)
if created:
    course.students.add(student)
    print(f'  + Course created: {course.title}')
else:
    print(f'  - Course exists: {course.title}')
    if student not in course.students.all():
        course.students.add(student)
        print('    + Student added to course')

# 3. Удаляем старые уроки и создаём новые с правильными ID
print('\n3. Creating lessons...')
Lesson.objects.filter(course=course).delete()
print('  - Old lessons removed')

lessons_data = [
    {
        'title': 'Introduction to Python',
        'video_url': 'https://www.youtube.com/watch?v=kqtD5dpn9C8',
        'content': '''Welcome to Python programming!

In this lesson you will learn:
- What is Python and why is it popular
- Where Python is used in real world
- Basic Python capabilities
- Your first "Hello, World!" program

After watching the video, install Python and try the examples.''',
        'order': 1,
    },
    {
        'title': 'Variables and Data Types',
        'video_url': 'https://www.youtube.com/watch?v=Z1Yd7upQsXY',
        'content': '''Learn about variables and data types.

Topics covered:
- What are variables and how to create them
- Basic data types: numbers, strings, booleans
- Operations with different data types
- Type conversion

Practice: create variables of different types and perform operations.''',
        'order': 2,
    },
    {
        'title': 'Conditional Statements (if-elif-else)',
        'video_url': 'https://www.youtube.com/watch?v=f4KOjWS_KZs',
        'content': '''Master conditional logic in Python.

In this lesson:
- Conditional operators and logical expressions
- if statement syntax
- Using elif for multiple conditions
- else as alternative
- Nested conditions

Task: write a program that determines user age category.''',
        'order': 3,
    },
]

for data in lessons_data:
    lesson = Lesson.objects.create(
        course=course,
        title=data['title'],
        video_url=data['video_url'],
        content=data['content'],
        order=data['order'],
    )
    print(f'  + Lesson {lesson.id}: {lesson.title}')

# 4. Создаём класс
print('\n4. Creating class...')
class_group, created = ClassGroup.objects.get_or_create(
    name='10-A',
    defaults={
        'class_teacher': teacher,
    }
)
if created:
    class_group.students.add(student)
    print(f'  + Class created: {class_group.name}')
else:
    print(f'  - Class exists: {class_group.name}')

print('\n' + '='*60)
print('LOCAL DATABASE SETUP COMPLETE!')
print('='*60)
print(f'\nAccess the application:')
print(f'  URL: http://127.0.0.1:8000')
print(f'  Admin: http://127.0.0.1:8000/admin')
print(f'\nTest accounts:')
print(f'  Admin:   admin / admin123')
print(f'  Teacher: teacher / teacher123')
print(f'  Student: student / student123')
print(f'\nCourse: {course.title}')
print(f'Lessons: {course.lessons.count()}')
print(f'\nFirst lesson URL: http://127.0.0.1:8000/lesson/{course.lessons.first().id}/')
print('='*60)
