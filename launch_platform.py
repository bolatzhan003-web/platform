import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lms.settings')
django.setup()

from django.contrib.auth import get_user_model
from core.models import Course, Lesson, ClassGroup, LessonMaterial

User = get_user_model()

print('='*70)
print('LAUNCHING LMS PLATFORM - FULL SETUP')
print('='*70)
print(f'Date: 2026-08-12')
print(f'Time: 10:22 UTC')
print('='*70)

# 1. ПОЛЬЗОВАТЕЛИ
print('\n[1/5] Creating users...')

admin, created = User.objects.get_or_create(
    username='admin',
    defaults={
        'email': 'admin@lms.platform',
        'first_name': 'System',
        'last_name': 'Administrator',
        'role': 'admin',
        'is_staff': True,
        'is_superuser': True,
    }
)
if created:
    admin.set_password('admin123')
    admin.save()
    print('  + Admin: admin / admin123')
else:
    print('  - Admin exists')

# Учителя
teachers_data = [
    {'username': 'teacher', 'first_name': 'Ivan', 'last_name': 'Petrov', 'email': 'ivan@lms.platform'},
    {'username': 'teacher2', 'first_name': 'Maria', 'last_name': 'Ivanova', 'email': 'maria@lms.platform'},
]

teachers = []
for data in teachers_data:
    teacher, created = User.objects.get_or_create(
        username=data['username'],
        defaults={
            'email': data['email'],
            'first_name': data['first_name'],
            'last_name': data['last_name'],
            'role': 'teacher',
            'is_staff': True,
        }
    )
    if created:
        teacher.set_password('teacher123')
        teacher.save()
        print(f'  + Teacher: {data["username"]} / teacher123')
    else:
        print(f'  - Teacher exists: {data["username"]}')
    teachers.append(teacher)

# Ученики
students_data = [
    {'username': 'student', 'first_name': 'Aliya', 'last_name': 'Nurlanova', 'email': 'aliya@student.kz'},
    {'username': 'student2', 'first_name': 'Dias', 'last_name': 'Bekbolat', 'email': 'dias@student.kz'},
    {'username': 'student3', 'first_name': 'Aigerim', 'last_name': 'Suleimenova', 'email': 'aigerim@student.kz'},
]

students = []
for data in students_data:
    student, created = User.objects.get_or_create(
        username=data['username'],
        defaults={
            'email': data['email'],
            'first_name': data['first_name'],
            'last_name': data['last_name'],
            'role': 'student',
        }
    )
    if created:
        student.set_password('student123')
        student.save()
        print(f'  + Student: {data["username"]} / student123')
    else:
        print(f'  - Student exists: {data["username"]}')
    students.append(student)

# 2. КЛАССЫ
print('\n[2/5] Creating classes...')

classes_data = [
    {'name': '10-A', 'teacher': teachers[0], 'students': students[:2]},
    {'name': '11-B', 'teacher': teachers[1], 'students': students[1:]},
]

for data in classes_data:
    class_group, created = ClassGroup.objects.get_or_create(
        name=data['name'],
        defaults={'class_teacher': data['teacher']}
    )
    if created:
        class_group.students.set(data['students'])
        print(f'  + Class: {data["name"]} - {len(data["students"])} students')
    else:
        print(f'  - Class exists: {data["name"]}')

# 3. КУРСЫ И УРОКИ
print('\n[3/5] Creating courses and lessons...')

courses_data = [
    {
        'title': 'Python Programming Basics',
        'description': 'Complete Python course for beginners. Learn programming from scratch with video lessons and practice materials.',
        'author': teachers[0],
        'students': students,
        'lessons': [
            {
                'title': '1. Introduction to Python',
                'video_url': 'https://www.youtube.com/watch?v=kqtD5dpn9C8',
                'content': '''Welcome to Python programming!

**What you will learn:**
- What is Python and why learn it
- Installing Python on your computer
- Writing your first program
- Basic Python syntax

**Duration:** 6 minutes

After this lesson, you will be ready to write simple Python programs.''',
                'order': 1,
            },
            {
                'title': '2. Variables and Data Types',
                'video_url': 'https://www.youtube.com/watch?v=Z1Yd7upQsXY',
                'content': '''Master Python variables and data types.

**Topics covered:**
- What are variables
- Integers, floats, strings, booleans
- Type conversion
- Basic operations

**Practice:**
Create variables of different types and perform operations with them.''',
                'order': 2,
            },
            {
                'title': '3. Conditional Statements',
                'video_url': 'https://www.youtube.com/watch?v=f4KOjWS_KZs',
                'content': '''Learn conditional logic in Python.

**In this lesson:**
- if, elif, else statements
- Comparison operators
- Logical operators (and, or, not)
- Nested conditions

**Task:**
Write a program that determines if a number is positive, negative, or zero.''',
                'order': 3,
            },
            {
                'title': '4. Loops and Iterations',
                'video_url': 'https://www.youtube.com/watch?v=94UHCEmprCY',
                'content': '''Master loops in Python.

**Topics:**
- for loops
- while loops
- range() function
- break and continue statements
- Loop best practices

**Practice:**
Create a program that prints numbers from 1 to 100.''',
                'order': 4,
            },
        ]
    },
    {
        'title': 'Web Development with HTML & CSS',
        'description': 'Learn to create beautiful websites from scratch. HTML structure, CSS styling, responsive design.',
        'author': teachers[1],
        'students': students[:2],
        'lessons': [
            {
                'title': '1. HTML Basics',
                'video_url': 'https://www.youtube.com/watch?v=UB1O30fR-EE',
                'content': '''Introduction to HTML.

**You will learn:**
- What is HTML
- HTML document structure
- Basic tags
- Creating your first webpage

Start building websites today!''',
                'order': 1,
            },
            {
                'title': '2. CSS Fundamentals',
                'video_url': 'https://www.youtube.com/watch?v=1Rs2ND1ryYc',
                'content': '''Style your websites with CSS.

**Topics:**
- What is CSS
- Selectors
- Colors and fonts
- Box model
- Layout basics

Make your websites beautiful!''',
                'order': 2,
            },
        ]
    },
]

for course_data in courses_data:
    course, created = Course.objects.get_or_create(
        title=course_data['title'],
        defaults={
            'description': course_data['description'],
            'author': course_data['author'],
        }
    )

    if created:
        course.students.set(course_data['students'])
        print(f'\n  + Course: {course.title}')
        print(f'    Author: {course.author.get_full_name()}')
        print(f'    Students: {course.students.count()}')

        # Создаём уроки
        for lesson_data in course_data['lessons']:
            lesson = Lesson.objects.create(
                course=course,
                title=lesson_data['title'],
                video_url=lesson_data['video_url'],
                content=lesson_data['content'],
                order=lesson_data['order'],
            )
            print(f'    + Lesson: {lesson.title}')
    else:
        print(f'  - Course exists: {course.title}')

# 4. СТАТИСТИКА
print('\n[4/5] Platform statistics:')
print(f'  Users: {User.objects.count()}')
print(f'    - Admins: {User.objects.filter(role="admin").count()}')
print(f'    - Teachers: {User.objects.filter(role="teacher").count()}')
print(f'    - Students: {User.objects.filter(role="student").count()}')
print(f'  Classes: {ClassGroup.objects.count()}')
print(f'  Courses: {Course.objects.count()}')
print(f'  Lessons: {Lesson.objects.count()}')
print(f'  Materials: {LessonMaterial.objects.count()}')

# 5. ДОСТУП
print('\n[5/5] Access information:')
print(f'  URL: http://127.0.0.1:8000')
print(f'  Admin Panel: http://127.0.0.1:8000/admin')
print()
print('  Test Accounts:')
print('  +-------------------------------------------+')
print('  | Role      | Login     | Password        |')
print('  +-------------------------------------------+')
print('  | Admin     | admin     | admin123        |')
print('  | Teacher   | teacher   | teacher123      |')
print('  | Teacher 2 | teacher2  | teacher123      |')
print('  | Student   | student   | student123      |')
print('  | Student 2 | student2  | student123      |')
print('  | Student 3 | student3  | student123      |')
print('  +-------------------------------------------+')

print('\n' + '='*70)
print('LMS PLATFORM IS READY!')
print('='*70)
print('\nNext steps:')
print('1. Open http://127.0.0.1:8000 in your browser')
print('2. Login as student/teacher/admin')
print('3. Explore courses, watch videos, upload materials')
print('4. Test all features before production deployment')
print('\nFor production deployment:')
print('  - Run: switch-env.bat prod')
print('  - Update DJANGO_SECRET_KEY in .env')
print('  - Deploy to Render.com')
print('='*70)
