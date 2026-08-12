from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html

from .models import (
    ClassGroup,
    Course,
    Lesson,
    LessonMaterial,
    LessonProgress,
    News,
    PlatformSettings,
    User,
)


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    """Управления пользователями: удобный просмотр ролей и поиск."""

    list_display = ('username', 'first_name', 'phone', 'role', 'is_staff', 'is_active')
    list_filter = ('role', 'is_staff', 'is_active')
    search_fields = ('username', 'first_name', 'last_name', 'email', 'phone')
    ordering = ('username',)

    fieldsets = UserAdmin.fieldsets + (
        ('Роль и платформа', {'fields': ('role', 'phone')}),
    )


class LessonInline(admin.TabularInline):
    model = Lesson
    extra = 1


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    """Курсы. filter_horizontal позволяет удобно выдавать доступ ученикам."""

    list_display = ('title', 'author', 'lesson_count', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('title', 'description', 'author__username', 'author__last_name')
    filter_horizontal = ('students',)
    autocomplete_fields = ('author',)
    inlines = [LessonInline]
    fieldsets = (
        ('Основное', {'fields': ('title', 'description', 'cover')}),
        ('Автор и доступ', {'fields': ('author', 'students')}),
    )


class LessonMaterialInline(admin.TabularInline):
    model = LessonMaterial
    extra = 1


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'order', 'video_url')
    list_editable = ('order',)
    list_filter = ('course',)
    search_fields = ('title', 'content', 'course__title')
    inlines = [LessonMaterialInline]


@admin.register(LessonMaterial)
class LessonMaterialAdmin(admin.ModelAdmin):
    list_display = ('display_name', 'lesson', 'uploaded_at')
    list_filter = ('lesson__course',)
    search_fields = ('title', 'file', 'lesson__title')

    def has_add_permission(self, request):
        # Файлы удобнее загружать из урока, но в админке тоже можно
        return True


@admin.register(LessonProgress)
class LessonProgressAdmin(admin.ModelAdmin):
    list_display = ('student', 'lesson', 'opened_at', 'completed_at')
    list_filter = ('lesson__course', 'opened_at')
    search_fields = ('student__username', 'student__last_name', 'lesson__title')

    def has_add_permission(self, request):
        return False  # прогресс создаётся автоматически

    def has_change_permission(self, request, obj=None):
        return False  # и меняется автоматически


@admin.register(ClassGroup)
class ClassGroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'class_teacher', 'student_count')
    search_fields = ('name', 'class_teacher__username', 'class_teacher__last_name')
    autocomplete_fields = ('class_teacher',)
    filter_horizontal = ('students',)

    @admin.display(description='Учеников')
    def student_count(self, obj):
        return obj.students.count()


@admin.register(PlatformSettings)
class PlatformSettingsAdmin(admin.ModelAdmin):
    list_display = ('name',)

    def has_add_permission(self, request):
        return not PlatformSettings.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_active', 'order', 'created_at', 'preview_link')
    list_filter = ('is_active', 'created_at')
    list_editable = ('order', 'is_active')
    search_fields = ('title', 'description')

    fieldsets = (
        ('Основное', {'fields': ('title', 'image', 'description')}),
        ('Ссылка (опционально)', {'fields': ('link', 'link_text')}),
        ('Видимость', {'fields': ('is_active', 'order')}),
    )

    @admin.display(description='Ссылка')
    def preview_link(self, obj):
        if obj.link:
            return format_html('<a href="{}" target="_blank">Открыть →</a>', obj.link)
        return '—'