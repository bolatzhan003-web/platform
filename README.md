# 🎓 LMS — Образовательная платформа на Django

Готовая к запуску LMS: курсы, видеоуроки (YouTube/Vimeo) с загружаемыми файлами-материалами, роли ученик/учитель/админ.
Проект настроен для деплоя на **Render** (веб-сервис) + **Supabase** (PostgreSQL).

---

## 🚀 Быстрый старт локально

### 1. Подготовка окружения

```bash
# создать виртуальное окружение
python -m venv venv

# активация (Windows PowerShell)
venv\Scripts\activate
# активация (Linux/macOS / Git Bash)
# source venv/bin/activate

# зависимости
pip install -r requirements.txt
```

### 2. Файл окружения

```bash
cp .env.example .env
```

В `.env` укажите `DJANGO_SECRET_KEY` и при необходимости `DATABASE_URL`.
Без `DATABASE_URL` проект работает на локальном SQLite — для разработки этого достаточно.

### 3. Миграции, статика, суперпользователь

```bash
python manage.py makemigrations core
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py createsuperuser
```

### 4. Запуск

```bash
python manage.py runserver
```

Открыть: http://127.0.0.1:8000 · Админ-панель: http://127.0.0.1:8000/admin

### Демо-данные

В папке проекта лежит готовая локальная база `db.sqlite3` с тестовыми данными:

| Роль | Логин | Пароль | Что видит |
|---|---|---|---|
| Админ | `admin` | `adminpass123` | упр-е всем через /admin |
| Учитель | `teacher` | `teacherpass123` | свои курсы и классы |
| Ученик (с доступом) | `student` | `studentpass123` | курсы с видеоуроками и материалами |
| Ученик (без доступа) | `outsider` | `outsiderpass123` | при попытке открыть курс — «Доступ закрыт» |

> Чтобы начать с чистой базы — удалите `db.sqlite3` и выполните `migrate` + `createsuperuser` заново.

---

## 🧱 Структура проекта

```
lms/
├── manage.py
├── requirements.txt        # зависимости
├── Procfile                # команда запуска для Render
├── render.yaml             # blueprint для Render
├── .env.example            # шаблон переменных окружения
├── lms/                    # настройки проекта
│   ├── settings.py         # python-dotenv + dj-database-url + whitenoise
│   ├── urls.py
│   ├── wsgi.py / asgi.py
├── core/                   # приложение
│   ├── models.py           # User, ClassGroup, Course, Lesson, LessonMaterial
│   ├── admin.py            # регистрация моделей, filter_horizontal
│   ├── views.py            # доступы, дашборды, уроки, материалы
│   └── urls.py
├── templates/              # шаблоны (base, dashboards, courses)
├── staticfiles/            # собранная статика (whitenoise)
└── db.sqlite3              # локальная БД (не в git)
```

### Модели

- **User** — кастомный `AbstractUser` с полем `role` (student / teacher / admin).
- **ClassGroup** — класс: название, классный руководитель (FK), ученики (M2M).
- **Course** — курс: название, описание, автор-учитель, `students` (M2M — ручная выдача доступа).
- **Lesson** — урок: курс (FK), заголовок, `video_url` (YouTube/Vimeo), текст, порядок.
- **LessonMaterial** — файл-материал к уроку: урок (FK), название, файл, дата загрузки.

### Логика доступа

- Ученик видит уроки курса **только если добавлен в `students` этого курса**. Иначе — редирект на страницу «🔒 Доступ закрыт».
- Учитель (автор курса / staff) может **загружать и удалять файлы-материалы** прямо на странице урока. Ученик их видит и скачивает.
- Дашборд ученика: его курсы, количество уроков и материалов.
- Дашборд учителя: его курсы и классы (+ быстрые ссылки на создание в админке).

---

## ☁️ Деплой на Render + Supabase

### 1. База данных Supabase

1. Зарегистрируйтесь на [supabase.com](https://supabase.com) и создайте проект (свободный тариф Free).
2. Перейдите **Project Settings → Database → Connection string**.
3. Скопируйте **URI** подключения (вид `postgresql://postgres.<ref>:<password>@aws-0-<region>.pooler.supabase.com:6543/postgres`).
4. Добавьте параметр `?sslmode=require` в конец URL (Supabase просит SSL).

### 2. Веб-сервис на Render

**Вариант A — через blueprint `render.yaml`** (лежит в корне проекта):

1. [render.com](https://render.com) → **New → Blueprint** → подключите репозиторий.
2. Render сам создаст сервис из `render.yaml`. Для `DATABASE_URL` нажмите **"Connect Resource"** и укажите значение из Supabase вручную (поле со `sync: false`).

**Вариант B — вручную:**

1. **New → Web Service** → подключите свой Git-репозиторий.
2. Настройки:
   - **Runtime**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate`
   - **Start Command**: `gunicorn lms.wsgi:application --bind 0.0.0.0:$PORT --workers 2 --timeout 120`
3. **Environment variables**:

   | Переменная | Значение |
   |---|---|
   | `DJANGO_SECRET_KEY` | длинная случайная строка (генератор: `python -c "import secrets; print(secrets.token_urlsafe(50))"`) |
   | `DJANGO_DEBUG` | `False` |
   | `ALLOWED_HOSTS` | `.onrender.com,localhost,127.0.0.1` |
   | `DATABASE_URL` | `postgresql://...` из Supabase с `?sslmode=require` |

4. **Deploy**. Убедитесь, что в логах сервиса прошли `migrate` и `collectstatic`.

### 3. После деплоя

Выполните через Shell Render (или локально, направив `DATABASE_URL` на Supabase):

```bash
python manage.py createsuperuser
```

Сайт: `https://<ваш-сервис>.onrender.com` · Админ-панель: `/admin`

### Терминальные команды (шпаргалка)

```bash
# миграции
python manage.py makemigrations core
python manage.py migrate

# статика
python manage.py collectstatic --noinput

# суперпользователь
python manage.py createsuperuser
```

---

## 🔧 Технологии

Django 5.2 · PostgreSQL (dj-database-url) · whitenoise · gunicorn · python-dotenv · psycopg2.