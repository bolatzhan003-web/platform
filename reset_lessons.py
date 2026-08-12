import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lms.settings')
django.setup()

from core.models import Course, Lesson

# Получаем все курсы
courses = Course.objects.all()
print('Existing courses:')
for course in courses:
    print(f'  - {course.title}')

print('\n' + '='*60)

# Работаем с курсом Python
course = Course.objects.first()
print(f'\nWorking with: {course.title}')
print(f'Lessons count: {course.lessons.count()}')

# Удаляем все старые уроки
Lesson.objects.filter(course=course).delete()
print('\nOld lessons deleted.')

# Создаём новые уроки с проверенными видео
lessons_data = [
    {
        'title': 'Test Video - Me at the zoo',
        'video_url': 'https://www.youtube.com/watch?v=jNQXAC9IVRw',
        'content': 'First video on YouTube - always embeddable. Duration: 19 seconds.',
        'order': 1,
    },
    {
        'title': 'Python Tutorial for Beginners',
        'video_url': 'https://www.youtube.com/watch?v=kqtD5dpn9C8',
        'content': 'Learn Python basics from scratch.',
        'order': 2,
    },
]

print('\nCreating new lessons:')
for data in lessons_data:
    lesson = Lesson.objects.create(
        course=course,
        title=data['title'],
        video_url=data['video_url'],
        content=data['content'],
        order=data['order'],
    )
    video_id = lesson.video_url.split('=')[-1] if '=' in lesson.video_url else 'unknown'
    print(f'  + {lesson.title}')
    print(f'    Video ID: {video_id}')
    print(f'    Embed URL: {lesson.embed_url()}')

print('\n' + '='*60)
print('SUCCESS! Lessons updated.')
print('Refresh browser: http://127.0.0.1:8000')
print('Login as student: student / student123')
print('='*60)
