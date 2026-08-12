# 🎯 БЫСТРЫЙ СТАРТ - LMS Платформа

## 📋 Что создано

✅ Полнофункциональная LMS на Django  
✅ YouTube видеоплеер с автоотслеживанием прогресса  
✅ Подключение к Supabase PostgreSQL  
✅ Конфигурации для локальной разработки и продакшена  
✅ Тестовые данные и пользователи  

---

## 🚀 ЛОКАЛЬНАЯ РАЗРАБОТКА (SQLite)

### Переключиться на локальное окружение:

**Windows:**
```bash
switch-env.bat local
```

**Linux/Mac:**
```bash
./switch-env.sh local
```

**Или вручную:**
```bash
cp .env.local .env
```

### Запустить сервер:

```bash
# Активировать виртуальное окружение
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac

# Запустить
python manage.py runserver
```

Откройте: **http://127.0.0.1:8000**

### Тестовые аккаунты:

| Роль | Логин | Пароль |
|------|-------|--------|
| Админ | `admin` | `admin123` |
| Учитель | `teacher` | `teacher123` |
| Ученик | `student` | `student123` |

---

## 🌐 PRODUCTION ДЕПЛОЙ (Render + Supabase)

### 1. Переключиться на production окружение:

**Windows:**
```bash
switch-env.bat prod
```

**Linux/Mac:**
```bash
./switch-env.sh prod
```

**Или вручную:**
```bash
cp .env.production .env
```

### 2. Отредактировать .env:

⚠️ **ОБЯЗАТЕЛЬНО** обновите в `.env`:

```bash
# Сгенерируйте новый секретный ключ:
python -c "import secrets; print(secrets.token_urlsafe(50))"

# Вставьте результат в .env:
DJANGO_SECRET_KEY=ваш-новый-секретный-ключ
```

### 3. Деплой на Render.com:

#### Вариант A: Blueprint (быстро)

1. Залейте код в GitHub
2. [render.com](https://render.com) → **New → Blueprint**
3. Подключите репозиторий
4. Render автоматически развернёт из `render.yaml`
5. Добавьте `DATABASE_URL` в Environment Variables

#### Вариант B: Вручную

1. **New → Web Service** на Render
2. **Build Command:**
   ```
   pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate
   ```
3. **Start Command:**
   ```
   gunicorn lms.wsgi:application --bind 0.0.0.0:$PORT --workers 2 --timeout 120
   ```
4. **Environment Variables:**
   - `DJANGO_SECRET_KEY` = ваш секретный ключ
   - `DJANGO_DEBUG` = `False`
   - `ALLOWED_HOSTS` = `.onrender.com`
   - `DATABASE_URL` = ваш Supabase URL

### 4. Создать суперпользователя на продакшене:

```bash
# В Render Shell:
python manage.py createsuperuser
```

---

## 📁 Структура файлов

```
lms/
├── .env                  ← Активная конфигурация (не в git)
├── .env.local           ← Локальная разработка (SQLite)
├── .env.production      ← Production (Supabase PostgreSQL)
├── .env.example         ← Шаблон
├── switch-env.bat       ← Переключатель окружений (Windows)
├── switch-env.sh        ← Переключатель окружений (Linux/Mac)
├── DEPLOYMENT.md        ← Полная документация
├── requirements.txt     ← Зависимости
├── render.yaml          ← Blueprint для Render
├── Procfile            ← Команда запуска
├── manage.py
├── lms/                ← Настройки Django
├── core/               ← Приложение (models, views, admin)
├── templates/          ← HTML шаблоны
├── static/             ← CSS, JS
└── media/              ← Загруженные файлы
```

---

## 🎥 YouTube плеер

### Поддерживаемые форматы ссылок:

- `https://www.youtube.com/watch?v=VIDEO_ID`
- `https://youtu.be/VIDEO_ID`

### Решение ошибки 153:

Если появляется "Ошибка 153" (видео запретило встраивание):

1. Используйте кнопку **"📺 Открыть на YouTube"**
2. Выбирайте видео с образовательных каналов:
   - freeCodeCamp
   - Corey Schafer
   - Programming with Mosh
   - Официальные каналы языков программирования

---

## 🔄 Переключение окружений

### Текущее окружение (production):

- Database: **Supabase PostgreSQL**
- DEBUG: **False**
- URL: https://your-app.onrender.com

### Переключиться на локальное:

```bash
switch-env.bat local  # Windows
./switch-env.sh local # Linux/Mac
python manage.py runserver
```

---

## 🛠️ Полезные команды

```bash
# Миграции
python manage.py makemigrations
python manage.py migrate

# Создать админа
python manage.py createsuperuser

# Собрать статику
python manage.py collectstatic

# Запустить сервер
python manage.py runserver

# Создать тестовые данные
python create_test_course.py

# Сбросить уроки
python reset_lessons.py
```

---

## 📞 Поддержка

Полная документация: **DEPLOYMENT.md**

**Текущий статус:**
- ✅ Supabase подключен
- ✅ YouTube плеер настроен
- ✅ Тестовые данные загружены
- ✅ Локальный и production конфиги готовы
- 🚀 Готов к деплою!

---

**Создано:** 2026-08-12  
**Stack:** Django 5.2 · PostgreSQL · Supabase · Render · YouTube API
