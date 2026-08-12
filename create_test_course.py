import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lms.settings')
django.setup()

from django.contrib.auth import get_user_model
from core.models import Course, Lesson, ClassGroup

User = get_user_model()

# Получаем админа
admin = User.objects.get(username='admin')

# Создаем учителя, если нет
teacher, created = User.objects.get_or_create(
    username='teacher',
    defaults={
        'email': 'teacher@example.com',
        'first_name': 'Иван',
        'last_name': 'Петров',
        'role': 'teacher',
        'is_staff': True,
    }
)
if created:
    teacher.set_password('teacher123')
    teacher.save()
    print(f'Создан учитель: teacher / teacher123')

# Создаем ученика, если нет
student, created = User.objects.get_or_create(
    username='student',
    defaults={
        'email': 'student@example.com',
        'first_name': 'Алия',
        'last_name': 'Нурланова',
        'role': 'student',
    }
)
if created:
    student.set_password('student123')
    student.save()
    print(f'Создан ученик: student / student123')

# Создаем тестовый курс
course, created = Course.objects.get_or_create(
    title='Основы программирования на Python',
    defaults={
        'description': 'Изучите основы Python с нуля. Курс включает видеоуроки с YouTube и практические материалы.',
        'author': teacher,
    }
)
if created:
    course.students.add(student)
    print(f'Создан курс: {course.title}')
else:
    print(f'Курс уже существует: {course.title}')

# Создаем уроки с YouTube видео
lessons_data = [
    {
        'title': 'Введение в Python - Что это и зачем?',
        'video_url': 'https://www.youtube.com/watch?v=rfscVS0vtbw',
        'content': '''В этом уроке вы узнаете:
- Что такое Python и почему он так популярен
- Где используется Python в реальной жизни
- Как установить Python на свой компьютер
- Первая программа "Hello, World!"

После просмотра видео рекомендуется установить Python и повторить примеры из урока.''',
        'order': 1,
    },
    {
        'title': 'Переменные и типы данных',
        'video_url': 'https://youtu.be/rfscVS0vtbw',
        'content': '''Основные темы урока:
- Что такое переменные и как их создавать
- Основные типы данных: числа, строки, булевы значения
- Операции с разными типами данных
- Преобразование типов

Практика: создайте переменные разных типов и выполните операции с ними.''',
        'order': 2,
    },
    {
        'title': 'Условные операторы if-elif-else',
        'video_url': 'https://www.youtube.com/watch?v=AWek49wXGzI',
        'content': '''В этом уроке:
- Условные операторы и логические выражения
- Оператор if и его синтаксис
- Использование elif для множественных условий
- Оператор else как альтернатива
- Вложенные условия

Задание: напишите программу, которая определяет возрастную категорию пользователя.''',
        'order': 3,
    },
]

for lesson_data in lessons_data:
    lesson, created = Lesson.objects.get_or_create(
        course=course,
        title=lesson_data['title'],
        defaults={
            'video_url': lesson_data['video_url'],
            'content': lesson_data['content'],
            'order': lesson_data['order'],
        }
    )
    if created:
        print(f'  + Урок создан: {lesson.title}')
    else:
        print(f'  - Урок существует: {lesson.title}')

print('\n' + '='*60)
print('Тестовый курс создан успешно!')
print('='*60)
print(f'\nВход в систему:')
print(f'  URL: http://127.0.0.1:8000')
print(f'  Админ: http://127.0.0.1:8000/admin')
print(f'\nУчетные записи:')
print(f'  Учитель: teacher / teacher123')
print(f'  Ученик: student / student123')
print(f'  Админ: admin / admin123')
print(f'\nКурс: {course.title}')
print(f'Уроков: {course.lessons.count()}')
