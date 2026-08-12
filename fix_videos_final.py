import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lms.settings')
django.setup()

from core.models import Course, Lesson

course = Course.objects.get(title='Osnovyi programmirovaniya na Python')

# Список гарантированно работающих embed видео
working_videos = [
    {
        'title': 'TEST: YouTube Player Check',
        'video_url': 'https://www.youtube.com/watch?v=jNQXAC9IVRw',
        'order': 0,
    },
    {
        'title': 'Python Introduction',
        'video_url': 'https://www.youtube.com/watch?v=Y8Tko2YC5hA',
        'order': 1,
    },
    {
        'title': 'Python Variables',
        'video_url': 'https://www.youtube.com/watch?v=8DvywoWv6zI',
        'order': 2,
    },
]

print('Updating lessons with embeddable videos...\n')

for data in working_videos:
    lesson, created = Lesson.objects.update_or_create(
        course=course,
        title=data['title'],
        defaults={
            'video_url': data['video_url'],
            'content': f'Video ID: {data["video_url"].split("=")[-1]}',
            'order': data['order'],
        }
    )
    status = 'Created' if created else 'Updated'
    print(f'{status}: {lesson.title}')
    print(f'  URL: {lesson.video_url}')
    print(f'  Embed: {lesson.embed_url()}\n')

print('Done! Refresh browser page (Ctrl+Shift+R)')
