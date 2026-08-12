import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lms.settings')
django.setup()

from core.models import Course, Lesson

course = Course.objects.get(title='Основы программирования на Python')

# Добавим тестовый урок с официальным тестовым видео YouTube
# Это видео 100% разрешает embed - используется для тестирования плееров
test_lesson, created = Lesson.objects.update_or_create(
    course=course,
    title='🧪 ТЕСТ: Проверка YouTube плеера',
    defaults={
        'video_url': 'https://www.youtube.com/watch?v=jNQXAC9IVRw',  # "Me at the zoo" - первое видео на YouTube, всегда доступно для embed
        'content': '''Это тестовый урок для проверки работы YouTube плеера.

Если вы видите это видео (первое видео, загруженное на YouTube в 2005 году),
значит плеер работает корректно.

Если видите ошибку 153, это означает:
- Ограничения сети/браузера блокируют YouTube embed
- Нужно использовать кнопку "Открыть на YouTube" для просмотра

Технические детали:
- Video ID: jNQXAC9IVRw
- Длительность: 19 секунд
- Статус: Публичное, embed разрешён''',
        'order': 0,
    }
)

if created:
    print('Test lesson created!')
else:
    print('Test lesson updated!')

print('\nTitle:', test_lesson.title)
print('URL:', test_lesson.video_url)
print('Embed:', test_lesson.embed_url())
print('\nThis is the first video on YouTube - it always works with embed.')
print('Open this lesson in browser to check.')
