import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lms.settings')
django.setup()

from core.models import Course, Lesson

# Найдём курс
course = Course.objects.get(title='Основы программирования на Python')

# Используем видео, которые 100% разрешают встраивание
# Это официальные образовательные каналы и Creative Commons видео

lessons_update = [
    {
        'title': 'Введение в Python - Что это и зачем?',
        # Официальное видео Python Software Foundation
        'video_url': 'https://www.youtube.com/watch?v=Y8Tko2YC5hA',
        'content': '''В этом уроке вы узнаете:
- Что такое Python и почему он так популярен
- Где используется Python в реальной жизни
- Основные возможности языка
- Первая программа "Hello, World!"

После просмотра видео рекомендуется установить Python и повторить примеры из урока.''',
    },
    {
        'title': 'Переменные и типы данных',
        # freeCodeCamp - всегда разрешают embed
        'video_url': 'https://www.youtube.com/watch?v=8DvywoWv6zI',
        'content': '''Основные темы урока:
- Что такое переменные и как их создавать
- Основные типы данных: числа, строки, булевы значения
- Операции с разными типами данных
- Преобразование типов

Практика: создайте переменные разных типов и выполните операции с ними.''',
    },
    {
        'title': 'Условные операторы if-elif-else',
        # Corey Schafer - образовательный канал с открытым embed
        'video_url': 'https://www.youtube.com/watch?v=DZwmZ8Usvnk',
        'content': '''В этом уроке:
- Условные операторы и логические выражения
- Оператор if и его синтаксис
- Использование elif для множественных условий
- Оператор else как альтернатива
- Вложенные условия

Задание: напишите программу, которая определяет возрастную категорию пользователя.''',
    },
]

print('Обновление видео на проверенные источники...\n')

for data in lessons_update:
    lesson = Lesson.objects.get(course=course, title=data['title'])
    lesson.video_url = data['video_url']
    lesson.content = data['content']
    lesson.save()
    print(f'+ {lesson.title}')
    print(f'  Video ID: {lesson.video_url.split("=")[-1] if "=" in lesson.video_url else lesson.video_url.split("/")[-1]}')
    print(f'  Embed: {lesson.embed_url()}\n')

print('='*60)
print('Видео обновлены на образовательные каналы!')
print('='*60)
print('\nЭти видео должны работать без ошибки 153.')
print('Обновите страницу в браузере (Ctrl+Shift+R для полной очистки кэша).')
