import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lms.settings')
django.setup()

from core.models import Course, Lesson

# Найдём созданный курс
course = Course.objects.get(title='Основы программирования на Python')

# Обновим видео на те, которые разрешают встраивание
# Используем официальные обучающие видео, которые разрешают embed

lessons_update = [
    {
        'title': 'Введение в Python - Что это и зачем?',
        'video_url': 'https://www.youtube.com/watch?v=kqtD5dpn9C8',  # Programming with Mosh - Python Tutorial
        'content': '''В этом уроке вы узнаете:
- Что такое Python и почему он так популярен
- Где используется Python в реальной жизни
- Основные возможности языка
- Первая программа "Hello, World!"

После просмотра видео рекомендуется установить Python и повторить примеры из урока.''',
    },
    {
        'title': 'Переменные и типы данных',
        'video_url': 'https://www.youtube.com/watch?v=Z1Yd7upQsXY',  # Variables in Python
        'content': '''Основные темы урока:
- Что такое переменные и как их создавать
- Основные типы данных: числа, строки, булевы значения
- Операции с разными типами данных
- Преобразование типов

Практика: создайте переменные разных типов и выполните операции с ними.''',
    },
    {
        'title': 'Условные операторы if-elif-else',
        'video_url': 'https://www.youtube.com/watch?v=f4KOjWS_KZs',  # If statements
        'content': '''В этом уроке:
- Условные операторы и логические выражения
- Оператор if и его синтаксис
- Использование elif для множественных условий
- Оператор else как альтернатива
- Вложенные условия

Задание: напишите программу, которая определяет возрастную категорию пользователя.''',
    },
]

for data in lessons_update:
    lesson = Lesson.objects.get(course=course, title=data['title'])
    lesson.video_url = data['video_url']
    lesson.content = data['content']
    lesson.save()
    print(f'Обновлено: {lesson.title}')
    print(f'  Новое видео: {lesson.video_url}')
    print(f'  Embed URL: {lesson.embed_url()}')
    print()

print('='*60)
print('Видео обновлены на те, которые разрешают встраивание!')
print('='*60)
print('Обновите страницу в браузере и проверьте плеер.')
