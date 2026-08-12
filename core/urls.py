from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

urlpatterns = [
    # Главная и вход/выход
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),

    # Дашборды по ролям
    path('student/', views.student_dashboard, name='student_dashboard'),
    path('teacher/', views.teacher_dashboard, name='teacher_dashboard'),

    # Курсы и уроки
    path('course/<int:pk>/', views.course_detail, name='course_detail'),
    path('lesson/<int:pk>/', views.lesson_detail, name='lesson_detail'),

    # Каталог и прогресс
    path('courses/', views.course_catalog, name='course_catalog'),
    path('progress/', views.my_progress, name='my_progress'),
    path('news/', views.news_list, name='news_list'),

    # Профиль и смена пароля
    path('profile/', views.profile, name='profile'),
    path('profile/avatar/', views.profile_update_avatar, name='profile_update_avatar'),
    path('password-change/', auth_views.PasswordChangeView.as_view(
        template_name='registration/password_change.html',
        success_url='/profile/',
    ), name='password_change'),

    # Доступ закрыт
    path('access-denied/', views.access_denied, name='access_denied'),
]