# 🎓 LMS — Образовательная платформа

Полнофункциональная LMS на Django с YouTube видеоуроками, загружаемыми материалами и системой ролей.

## 📋 Возможности

✅ **Курсы и уроки** с YouTube видео  
✅ **Загружаемые материалы** (PDF, Word, презентации)  
✅ **Система ролей**: ученик, учитель, админ  
✅ **Отслеживание прогресса** - автоматическая отметка завершения видео  
✅ **Управление доступом** к курсам  
✅ **Классы** с классными руководителями  
✅ **Готовность к production**: PostgreSQL (Supabase), gunicorn, whitenoise

---

## 🚀 Быстрый старт (локально)

### 1. Клонируйте репозиторий и создайте виртуальное окружение

```bash
git clone <your-repo-url>
cd lms

# Создать виртуальное окружение
python -m venv venv

# Активация (Windows)
venv\Scripts\activate

# Активация (Linux/macOS)
source venv/bin/activate

# Установить зависимости
pip install -r requirements.txt
```

### 2. Настройте окружение для локальной разработки

```bash
# Скопируйте локальный конфиг
cp .env.local .env
```

Файл `.env.local` настроен для работы с SQLite - ничего менять не нужно.

### 3. Выполните миграции и создайте суперпользователя

```bash
python manage.py migrate
python manage.py createsuperuser
```

### 4. (Опционально) Загрузите тестовые данные

```bash
python manage.py shell < create_test_course.py
```

### 5. Запустите сервер

```bash
python manage.py runserver
```

Откройте: **http://127.0.0.1:8000**

---

## 🌐 Деплой на Render + Supabase

### Шаг 1: Создайте базу данных на Supabase

1. Зарегистрируйтесь на [supabase.com](https://supabase.com)
2. Создайте новый проект
3. Перейдите: **Project Settings → Database → Connection string**
4. Скопируйте **URI** (формат: `postgresql://postgres:[PASSWORD]@[HOST]:5432/postgres`)
5. Добавьте `?sslmode=require` в конец URL

### Шаг 2: Разверните на Render

#### Вариант A: Через Blueprint (рекомендуется)

1. Залейте проект в GitHub
2. Откройте [render.com](https://render.com) → **New → Blueprint**
3. Подключите репозиторий
4. Render создаст сервис из файла `render.yaml`
5. В настройках добавьте переменную `DATABASE_URL` со значением из Supabase

#### Вариант B: Вручную

1. **New → Web Service** → подключите GitHub репозиторий
2. **Настройки:**
   - **Runtime**: Python 3
   - **Build Command**: 
     ```bash
     pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate
     ```
   - **Start Command**: 
     ```bash
     gunicorn lms.wsgi:application --bind 0.0.0.0:$PORT --workers 2 --timeout 120
     ```

3. **Environment Variables** (добавьте в Render):

   | Переменная | Значение |
   |---|---|
   | `DJANGO_SECRET_KEY` | Сгенерируйте: `python -c "import secrets; print(secrets.token_urlsafe(50))"` |
   | `DJANGO_DEBUG` | `False` |
   | `ALLOWED_HOSTS` | `.onrender.com,localhost` |
   | `DATABASE_URL` | `postgresql://...` (из Supabase с `?sslmode=require`) |

4. Нажмите **Create Web Service**

### Шаг 3: Создайте суперпользователя на продакшене

После успешного деплоя:

1. Откройте **Shell** в Render Dashboard
2. Выполните:
   ```bash
   python manage.py createsuperuser
   ```

Ваш сайт будет доступен по адресу: `https://your-app.onrender.com`

Админ-панель: `https://your-app.onrender.com/admin`

---

## 🔧 Переключение между окружениями

### Локальная разработка (SQLite)

```bash
cp .env.local .env
python manage.py runserver
```

### Production (Supabase PostgreSQL)

```bash
cp .env.production .env
# Отредактируйте .env и укажите реальный DJANGO_SECRET_KEY
python manage.py migrate
python manage.py runserver
```

---

## 📁 Структура проекта

```
lms/
├── manage.py
├── requirements.txt
├── Procfile                # Команда запуска для Render
├── render.yaml             # Blueprint конфигурация
├── .env.local              # Локальное окружение (SQLite)
├── .env.production         # Production окружение (PostgreSQL)
├── .env.example            # Шаблон переменных окружения
├── lms/                    # Настройки Django проекта
│   ├── settings.py         # Конфигурация (dotenv, dj-database-url, whitenoise)
│   ├── urls.py
│   └── wsgi.py
├── core/                   # Основное приложение
│   ├── models.py           # User, Course, Lesson, ClassGroup, LessonMaterial
│   ├── views.py            # Дашборды, уроки, доступ
│   ├── admin.py            # Админка с filter_horizontal
│   └── urls.py
├── templates/              # HTML шаблоны
│   ├── base.html
│   ├── courses/
│   │   ├── lesson_detail.html   # YouTube плеер + материалы
│   │   └── course_detail.html
│   └── dashboard/
├── static/                 # CSS, JS, изображения
├── staticfiles/            # Собранная статика (whitenoise)
├── media/                  # Загруженные файлы
└── db.sqlite3              # Локальная база данных (не в git)
```

---

## 🎯 Основные модели

### User
Кастомная модель с ролями: `student`, `teacher`, `admin`

### Course
Курс с автором (учитель) и списком учеников с доступом (M2M)

### Lesson
Урок с YouTube видео, текстовым контентом и порядковым номером

### LessonMaterial
Файлы-материалы к уроку (PDF, презентации, задания)

### ClassGroup
Класс с классным руководителем и списком учеников

### LessonProgress
Отслеживание прогресса: открытие урока и завершение

---

## 🎥 YouTube плеер

- Поддержка форматов: `youtube.com/watch?v=ID` и `youtu.be/ID`
- Автоматическая конвертация в embed URL
- YouTube IFrame API для отслеживания завершения видео
- Автоматическая отметка урока как пройденного после просмотра
- Запасная кнопка "Открыть на YouTube" если embed не работает

---

## 🔐 Роли и доступ

### Ученик
- Видит только курсы, в которые добавлен через `Course.students`
- Просматривает уроки и скачивает материалы
- Отслеживается прогресс по урокам

### Учитель
- Создаёт курсы (через админку)
- Загружает и удаляет материалы уроков
- Видит свои курсы и классы
- Может быть классным руководителем

### Администратор
- Полный доступ через Django Admin
- Управление пользователями, курсами, классами
- Назначение доступа к курсам через filter_horizontal

---

## 📦 Технологии

- **Backend**: Django 5.2, Python 3.12+
- **Database**: PostgreSQL (Supabase) / SQLite (dev)
- **Static Files**: WhiteNoise
- **WSGI Server**: Gunicorn
- **Frontend**: Vanilla JS, современный CSS с дизайн-системой
- **Video**: YouTube IFrame API

---

## 🛠️ Полезные команды

```bash
# Миграции
python manage.py makemigrations
python manage.py migrate

# Собрать статику
python manage.py collectstatic --noinput

# Создать суперпользователя
python manage.py createsuperuser

# Запустить сервер
python manage.py runserver

# Django shell
python manage.py shell

# Создать тестовые данные
python create_test_course.py
```

---

## 🎓 Тестовые аккаунты (после запуска create_test_course.py)

| Роль | Логин | Пароль | Описание |
|------|-------|--------|----------|
| Админ | `admin` | `admin123` | Полный доступ к админке |
| Учитель | `teacher` | `teacher123` | Управление своими курсами |
| Ученик | `student` | `student123` | Просмотр курсов с доступом |

---

## 📝 TODO / Будущие улучшения

- [ ] Поддержка загрузки видео напрямую на сервер
- [ ] Интеграция с S3/Cloudinary для media файлов
- [ ] Система тестов и заданий
- [ ] Чат между учителями и учениками
- [ ] Уведомления о новых уроках
- [ ] Статистика и аналитика для учителей
- [ ] Экспорт прогресса в Excel/PDF
- [ ] REST API для мобильного приложения

---

## 🐛 Решение проблем

### Ошибка YouTube 153 (embedding disabled)

Некоторые видео YouTube блокируют встраивание. Решения:
1. Используйте образовательные каналы (freeCodeCamp, Corey Schafer)
2. Проверьте настройки видео на YouTube
3. Используйте кнопку "Открыть на YouTube" как альтернативу

### База данных не подключается

Проверьте:
- Правильность `DATABASE_URL` в `.env`
- Наличие `?sslmode=require` для Supabase
- Доступность Supabase проекта

### Статические файлы не загружаются

```bash
python manage.py collectstatic --noinput
```

---

## 📄 Лицензия

MIT License - свободное использование для образовательных целей.

---

## 👨‍💻 Разработка

Создано с ❤️ для образования.

**Stack**: Django · PostgreSQL · Supabase · Render · YouTube API