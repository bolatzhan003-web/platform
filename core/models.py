from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    Кастомная модель пользователя с ролями: student / teacher / admin.

    Роль admin соответствует также is_staff/is_superuser в Django Admin.
    """

    ROLE_CHOICES = (
        ('student', 'Ученик'),
        ('teacher', 'Учитель'),
        ('admin', 'Администратор'),
    )

    role = models.CharField('Роль', max_length=20, choices=ROLE_CHOICES, default='student')
    phone = models.CharField('Номер телефона', max_length=20, blank=True, null=True, unique=True)
    created_at = models.DateTimeField('Дата регистрации', auto_now_add=True)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return f'{self.get_full_name() or self.username} ({self.get_role_display()})'

    # --- Удобные проверки роли ---
    @property
    def is_student(self):
        return self.role == 'student'

    @property
    def is_teacher(self):
        return self.role == 'teacher'

    @property
    def is_admin_role(self):
        return self.role == 'admin'


class ClassGroup(models.Model):
    """Класс: название, классный руководитель (учитель), список учеников."""

    name = models.CharField('Название класса', max_length=100)
    class_teacher = models.ForeignKey(
        User,
        verbose_name='Классный руководитель',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='class_groups_taught',
        limit_choices_to={'role': 'teacher'},
    )
    students = models.ManyToManyField(
        User,
        verbose_name='Ученики',
        related_name='class_groups',
        blank=True,
        limit_choices_to={'role': 'student'},
    )

    class Meta:
        verbose_name = 'Класс'
        verbose_name_plural = 'Классы'
        ordering = ['name']

    def __str__(self):
        return self.name


class Course(models.Model):
    """Курс: автор (учитель) + ручная выдача доступа ученикам через students."""

    title = models.CharField('Название курса', max_length=200)
    description = models.TextField('Описание', blank=True)
    author = models.ForeignKey(
        User,
        verbose_name='Автор (учитель)',
        on_delete=models.CASCADE,
        related_name='authored_courses',
        limit_choices_to={'role': 'teacher'},
    )
    students = models.ManyToManyField(
        User,
        verbose_name='Ученики с доступом',
        related_name='courses',
        blank=True,
        help_text='Выберите учеников, которым доступен курс.',
    )
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def lesson_count(self):
        return self.lessons.count()

    def progress_for(self, student):
        """Возвращает (открыто, завершено, всего, процент) для ученика по этому курсу."""
        lessons = self.lessons.all()
        total = lessons.count()
        opened = completed = 0
        if total and student.is_authenticated:
            records = {
                r.lesson_id: r
                for r in LessonProgress.objects.filter(student=student, lesson__course=self)
            }
            opened = sum(1 for l in lessons if l.pk in records)
            completed = sum(1 for l in lessons if records.get(l.pk) and records[l.pk].is_complete)
        pct = int(completed / total * 100) if total else 0
        return opened, completed, total, pct


class Lesson(models.Model):
    """Урок внутри курса: видео-ссылка (YouTube/Vimeo), текст и файлы-материалы."""

    course = models.ForeignKey(
        Course,
        verbose_name='Курс',
        on_delete=models.CASCADE,
        related_name='lessons',
    )
    title = models.CharField('Заголовок урока', max_length=200)
    video_url = models.URLField(
        'Видео YouTube',
        blank=True,
        help_text='Ссылка на YouTube видео (например: https://www.youtube.com/watch?v=dQw4w9WgXcQ или https://youtu.be/dQw4w9WgXcQ)',
    )
    content = models.TextField('Текстовый материал', blank=True)
    order = models.PositiveIntegerField('Порядок', default=0)

    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'
        ordering = ['order', 'id']

    def __str__(self):
        return f'{self.course.title} — {self.title}'

    def get_youtube_id(self):
        """Извлекает video ID из YouTube URL."""
        url = (self.video_url or '').strip()
        if not url:
            return None

        # Формат: https://youtu.be/VIDEO_ID
        if 'youtu.be' in url:
            video_id = url.rstrip('/').split('/')[-1].split('?')[0].split('&')[0]
            return video_id if len(video_id) == 11 else None

        # Формат: https://www.youtube.com/watch?v=VIDEO_ID
        if 'youtube.com' in url:
            from urllib.parse import parse_qs, urlparse
            qs = parse_qs(urlparse(url).query)
            video_id = (qs.get('v') or [None])[0]
            return video_id if video_id and len(video_id) == 11 else None

        return None

    def embed_url(self):
        """Возвращает URL видеоплеера (embed) для YouTube, иначе None."""
        video_id = self.get_youtube_id()
        if video_id:
            return f'https://www.youtube.com/embed/{video_id}?rel=0&modestbranding=1'
        return None

    def is_youtube(self):
        """Проверяет, что видео с YouTube."""
        return self.get_youtube_id() is not None


def lesson_material_path(instance, filename):
    """Путь хранения файлов: media/lessons/lesson_<id>/<имя файла>."""
    return f'lessons/lesson_{instance.lesson_id}/{filename}'


class LessonMaterial(models.Model):
    """Файл-материал, прикреплённый к видеоуроку (конспект, презентация, задание)."""

    lesson = models.ForeignKey(
        Lesson,
        verbose_name='Урок',
        on_delete=models.CASCADE,
        related_name='materials',
    )
    title = models.CharField(
        'Название',
        max_length=200,
        blank=True,
        help_text='Необязательно. По умолчанию показывается имя файла.',
    )
    file = models.FileField('Файл', upload_to=lesson_material_path)
    uploaded_at = models.DateTimeField('Дата загрузки', auto_now_add=True)

    class Meta:
        verbose_name = 'Материал урока'
        verbose_name_plural = 'Материалы уроков'
        ordering = ['-uploaded_at']

    def __str__(self):
        return self.title or self.file.name

    def display_name(self):
        """Человекочитаемое имя для показа ученику."""
        return self.title or self.file.name.rsplit('/', 1)[-1]


class LessonProgress(models.Model):
    """Отслеживание просмотра/усвоения урока конкретным учеником.

    Ученик «открыл» урок (первый просмотр) и считается «завершившим»,
    когда досмотрел видео (или, для урока без видео, открыл материалы).
    """

    student = models.ForeignKey(
        User,
        verbose_name='Ученик',
        on_delete=models.CASCADE,
        related_name='lesson_progress',
    )
    lesson = models.ForeignKey(
        Lesson,
        verbose_name='Урок',
        on_delete=models.CASCADE,
        related_name='progress_records',
    )
    opened_at = models.DateTimeField('Открыт', auto_now_add=True)
    completed_at = models.DateTimeField('Завершён', null=True, blank=True)

    class Meta:
        verbose_name = 'Прогресс урока'
        verbose_name_plural = 'Прогресс уроков'
        unique_together = ('student', 'lesson')
        ordering = ['-opened_at']

    def __str__(self):
        return f'{self.student.username} — {self.lesson.title}'

    @property
    def is_complete(self):
        return self.completed_at is not None