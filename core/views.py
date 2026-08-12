from functools import wraps

from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_http_methods
from django.db.models import Prefetch, Count

from .models import (
    Course,
    Lesson,
    LessonMaterial,
    LessonProgress,
    User,
)


# ---------------------------------------------------------------------------
# Вспомогательные функции доступа
# ---------------------------------------------------------------------------
def has_course_access(user, course):
    """Доступ к курсу имеют: автор, staff, и ученики из course.students."""
    if not user.is_authenticated:
        return False
    return user.is_staff or course.author_id == user.id or course.students.filter(pk=user.pk).exists()


def can_manage_course(user, course):
    """Материалы урока может менять: автор курса и staff."""
    return user.is_staff or course.author_id == user.id


def role_required(*roles):
    """Декоратор: разрешить доступ только пользователям с указанными ролями."""
    def decorator(view_func):
        @wraps(view_func)
        @login_required
        def _wrapped(request, *args, **kwargs):
            if request.user.role not in roles and not request.user.is_staff:
                return redirect('home')
            return view_func(request, *args, **kwargs)
        return _wrapped
    return decorator


def _get_or_create_progress(student, lesson):
    """Создаёт запись прогресса при первом открытии урока."""
    progress, created = LessonProgress.objects.get_or_create(
        student=student,
        lesson=lesson,
    )
    return progress, created


# ---------------------------------------------------------------------------
# Регистрация
# ---------------------------------------------------------------------------
@require_http_methods(['GET', 'POST'])
def register(request):
    """Регистрация нового пользователя через телефон."""
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        first_name = request.POST.get('first_name', '').strip()
        phone = request.POST.get('phone', '').strip()
        password1 = request.POST.get('password1', '')
        password2 = request.POST.get('password2', '')

        errors = []

        if not first_name:
            errors.append('Укажите имя')
        elif len(first_name) < 2:
            errors.append('Имя должно быть минимум 2 символа')

        if not phone:
            errors.append('Укажите номер телефона')
        elif User.objects.filter(phone=phone).exists():
            errors.append('Этот номер телефона уже зарегистрирован')

        if not password1:
            errors.append('Укажите пароль')
        elif len(password1) < 6:
            errors.append('Пароль должен быть минимум 6 символов')

        if password1 != password2:
            errors.append('Пароли не совпадают')

        if errors:
            return render(request, 'registration/register.html', {
                'first_name': first_name,
                'phone': phone,
                'errors': errors,
            })

        # Генерируем username из телефона
        username = f'user_{phone.replace("+", "").replace(" ", "").replace("-", "")}'

        user = User.objects.create_user(
            username=username,
            password=password1,
            first_name=first_name,
            phone=phone,
            role='student',
        )

        messages.success(request, 'Регистрация успешна! Теперь войдите в аккаунт.')
        return redirect('login')

    return render(request, 'registration/register.html')


@require_http_methods(['POST'])
def logout_view(request):
    """Выход из аккаунта через POST."""
    auth.logout(request)
    messages.success(request, 'Вы вышли из аккаунта.')
    return redirect('home')


# ---------------------------------------------------------------------------
# Главная / вход
# ---------------------------------------------------------------------------
def home(request):
    """Стартовая страница: логин -> дашборд, гость -> приветствие + вход."""
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'home.html')


@login_required
def dashboard(request):
    """Перенаправляет пользователя в дашборд по его роли."""
    if request.user.is_staff or request.user.is_admin_role:
        return redirect('admin:index')
    if request.user.is_teacher:
        return redirect('teacher_dashboard')
    return redirect('student_dashboard')


# ---------------------------------------------------------------------------
# Дашборд ученика
# ---------------------------------------------------------------------------
@role_required('student', 'teacher')
def student_dashboard(request):
    student = request.user
    courses = student.courses.prefetch_related('lessons').all()
    lessons_total = sum(c.lessons.count() for c in courses)
    materials_total = LessonMaterial.objects.filter(
        lesson__course__in=courses,
    ).count() if courses else 0
    progress_data = []
    for course in courses:
        opened, completed, total, pct = course.progress_for(student)
        progress_data.append({
            'course': course,
            'opened': opened,
            'completed': completed,
            'total': total,
            'pct': pct,
        })
    return render(request, 'dashboard/student.html', {
        'courses': courses,
        'lessons_total': lessons_total,
        'materials_total': materials_total,
        'progress_data': progress_data,
    })


# ---------------------------------------------------------------------------
# Дашборд учителя
# ---------------------------------------------------------------------------
@role_required('teacher')
def teacher_dashboard(request):
    teacher = request.user
    courses = Course.objects.filter(author=teacher)
    classes = teacher.class_groups_taught.all()
    # Уникальные ученики во всех курсах учителя
    student_count = User.objects.filter(
        courses__in=courses,
        role='student',
    ).distinct().count() if courses else 0
    return render(request, 'dashboard/teacher.html', {
        'courses': courses,
        'classes': classes,
        'student_count': student_count,
    })


# ---------------------------------------------------------------------------
# Каталог / все курсы
# ---------------------------------------------------------------------------
@login_required
def course_catalog(request):
    """Список ВСЕХ курсов платформы с пометкой «у меня есть доступ»."""
    user = request.user
    all_courses = Course.objects.all()
    my_ids = set(user.courses.values_list('id', flat=True)) if user.is_authenticated else set()
    catalog = []
    for course in all_courses:
        my = course.author_id == user.id or user.is_staff or course.id in my_ids
        opened, completed, total, pct = (0, 0, 0, 0)
        if my and user.role == 'student':
            opened, completed, total, pct = course.progress_for(user)
        catalog.append({
            'course': course,
            'is_mine': my,
            'pct': pct,
        })
    return render(request, 'courses/catalog.html', {
        'catalog': catalog,
    })


# ---------------------------------------------------------------------------
# Мой прогресс
# ---------------------------------------------------------------------------
@role_required('student', 'teacher')
def my_progress(request):
    """Сводка по усвоению/просмотру курсов учеником."""
    student = request.user
    courses = student.courses.all()
    progress = []
    total_opened = total_completed = total_lessons = 0
    for course in courses:
        opened, completed, total, pct = course.progress_for(student)
        total_opened += opened
        total_completed += completed
        total_lessons += total
        progress.append({
            'course': course,
            'opened': opened,
            'completed': completed,
            'total': total,
            'pct': pct,
        })
    overall_pct = int(total_completed / total_lessons * 100) if total_lessons else 0
    return render(request, 'dashboard/progress.html', {
        'progress': progress,
        'total_opened': total_opened,
        'total_completed': total_completed,
        'total_lessons': total_lessons,
        'overall_pct': overall_pct,
    })


# ---------------------------------------------------------------------------
# Профиль
# ---------------------------------------------------------------------------
@login_required
def profile(request):
    user = request.user
    progress_count = LessonProgress.objects.filter(
        student=user, completed_at__isnull=False,
    ).count() if user.role == 'student' else 0
    context = {
        'user': user,
        'progress_count': progress_count,
    }
    if user.role == 'student':
        context['courses_count'] = user.courses.count()
    if user.is_teacher or user.is_staff:
        context['course_count'] = Course.objects.filter(author=user).count() if not user.is_staff else Course.objects.count()
    return render(request, 'profile.html', context)


# ---------------------------------------------------------------------------
# Курсы и уроки
# ---------------------------------------------------------------------------
@role_required('student', 'teacher')
def course_detail(request, pk):
    course = get_object_or_404(Course, pk=pk)
    if not has_course_access(request.user, course):
        return redirect('access_denied')
    lessons = course.lessons.all()
    opened, completed, total, pct = course.progress_for(request.user)
    # ID завершённых уроков — для отметок «✓» в списке
    done_ids = set()
    if request.user.role == 'student':
        done_ids = set(LessonProgress.objects.filter(
            student=request.user,
            lesson__course=course,
            completed_at__isnull=False,
        ).values_list('lesson_id', flat=True))
    return render(request, 'courses/course_detail.html', {
        'course': course,
        'lessons': lessons,
        'pct': pct,
        'completed': completed,
        'total': total,
        'done_ids': done_ids,
    })


@role_required('student', 'teacher')
def lesson_detail(request, pk):
    lesson = get_object_or_404(Lesson, pk=pk)
    # Ключевая проверка: ученик видит урок только если он в students курса.
    if not has_course_access(request.user, lesson.course):
        return redirect('access_denied')

    can_manage = can_manage_course(request.user, lesson.course)

    # --- Действия ---
    action = request.POST.get('action')

    # Учитель / staff: загрузка и удаление материалов
    if request.method == 'POST' and action in ('upload', 'delete') and can_manage:
        if action == 'upload':
            uploaded = request.FILES.get('file')
            title = request.POST.get('title', '').strip()
            if uploaded:
                LessonMaterial.objects.create(
                    lesson=lesson,
                    title=title,
                    file=uploaded,
                )
                messages.success(request, f'Файл «{uploaded.name}» добавлен к уроку.')
            else:
                messages.error(request, 'Выберите файл для загрузки.')
        elif action == 'delete':
            material = LessonMaterial.objects.filter(
                pk=request.POST.get('material_id'),
                lesson=lesson,
            ).first()
            if material:
                material.file.delete(save=False)  # удаляем и файл с диска
                material.delete()
                messages.success(request, 'Материал удалён.')
        return redirect('lesson_detail', pk=lesson.pk)

    # Ученик: отметка «досмотрел видео» (вызывается JS-событием из плеера)
    if request.method == 'POST' and action == 'complete' and request.user.role == 'student':
        progress, _ = LessonProgress.objects.get_or_create(
            student=request.user, lesson=lesson,
        )
        if not progress.completed_at:
            from django.utils import timezone
            progress.completed_at = timezone.now()
            progress.save(update_fields=['completed_at'])
        return redirect('lesson_detail', pk=lesson.pk)

    # Ученик: фиксируем открытие урока (прогресс «просмотрен»)
    progress = None
    if request.user.role == 'student':
        progress, _ = _get_or_create_progress(request.user, lesson)

    materials = lesson.materials.all()
    lessons = lesson.course.lessons.all()
    return render(request, 'courses/lesson_detail.html', {
        'lesson': lesson,
        'course': lesson.course,
        'lessons': lessons,
        'materials': materials,
        'can_manage': can_manage,
        'progress': progress,
        'embed_url': lesson.embed_url(),
        'video_id': lesson.get_youtube_id(),
    })


# ---------------------------------------------------------------------------
# Доступ закрыт
# ---------------------------------------------------------------------------
def access_denied(request):
    return render(request, 'access_denied.html', status=403)