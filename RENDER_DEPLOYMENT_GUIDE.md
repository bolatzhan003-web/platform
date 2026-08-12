# 🚀 Полный гайд деплоя на Render.com

**Дата:** 2026-08-12  
**Статус:** Готово к деплою ✅

---

## ✅ Что уже готово

- ✅ Django приложение настроено
- ✅ Supabase PostgreSQL подключена
- ✅ `render.yaml` конфигурация готова
- ✅ `requirements.txt` со всеми зависимостями
- ✅ Все переменные окружения настроены

---

## 📋 ШАГ 1: Подготовка GitHub репозитория

### Если ещё не залили:

```bash
# Инициализировать git репозиторий
git init

# Добавить файлы
git add .

# Создать коммит
git commit -m "Initial commit: LMS with Django, Supabase, and Render deployment"

# Подключить GitHub репозиторий
git remote add origin https://github.com/YOUR_USERNAME/lms.git

# Залить на GitHub
git branch -M main
git push -u origin main
```

### Если уже залили:

Просто убедитесь что последний коммит на `main` ветке и пушните если есть изменения:

```bash
git push origin main
```

---

## 🔧 ШАГ 2: Генерация новых переменных для Production

Перед деплоем нужна новая `DJANGO_SECRET_KEY`. Откройте PowerShell/Terminal и выполните:

```bash
# Генерируем новый секретный ключ
python -c "import secrets; print(secrets.token_urlsafe(50))"
```

**Скопируйте результат** — он понадобится на следующем шаге.

---

## 🌐 ШАГ 3: Создание Web Service на Render.com

### 3.1 Войдите на render.com и нажмите "+ New"

![Step 1](https://via.placeholder.com/600x300?text=Step+1:+Click+New+Button)

### 3.2 Выберите "Web Service"

![Step 2](https://via.placeholder.com/600x300?text=Step+2:+Select+Web+Service)

### 3.3 Подключите GitHub репозиторий

- Нажмите "Connect a repository"
- Найдите `lms` репозиторий
- Нажмите "Connect"

![Step 3](https://via.placeholder.com/600x300?text=Step+3:+Connect+Repository)

### 3.4 Заполните данные сервиса

**Name:**
```
lms
```

**Environment:**
```
Python 3
```

**Build Command:**
```bash
pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate
```

**Start Command:**
```bash
gunicorn lms.wsgi:application --bind 0.0.0.0:$PORT --workers 2 --timeout 120
```

![Step 4](https://via.placeholder.com/600x300?text=Step+4:+Fill+Build+Commands)

### 3.5 Добавьте Environment Variables

Нажмите на "+ Add Environment Variable" для каждой:

| Ключ | Значение | Источник |
|------|----------|----------|
| `PYTHON_VERSION` | `3.12.10` | Зафиксированная версия |
| `DJANGO_SECRET_KEY` | `ваш-сгенерированный-ключ` | Из шага 2 ⬆️ |
| `DJANGO_DEBUG` | `False` | Production режим |
| `ALLOWED_HOSTS` | `.onrender.com` | Render домен |
| `DATABASE_URL` | `postgresql://postgres:29101997.1064sh@db.tugldzcyfvmqogquzvif.supabase.co:5432/postgres?sslmode=require` | Из `.env.production` |

![Step 5](https://via.placeholder.com/600x300?text=Step+5:+Add+Environment+Variables)

### 3.6 Нажмите "Create Web Service"

Деплой начнется автоматически. Это займет 5-10 минут.

![Step 6](https://via.placeholder.com/600x300?text=Step+6:+Create+Service)

---

## ⏳ ШАГ 4: Мониторинг деплоя

### На Dashboard Render:

1. Вы увидите статус деплоя: "Building..." → "Deploying..." → "Live"
2. Смотрите логи в realtime:
   - Зелёные логи = хорошо ✅
   - Красные логи = ошибка ❌

### Если есть ошибка с DATABASE_URL:

```
error: could not translate host name "db.tugldzcyfvmqogquzvif.supabase.co" to address
```

**Решение:** Проверьте что DATABASE_URL скопирована правильно (включая `?sslmode=require` в конце)

### Если есть ошибка с миграциями:

```
psycopg2.OperationalError: could not connect to server
```

**Решение:** Убедитесь что Supabase база доступна. Откройте Supabase → Project Settings → Database → проверьте что сервер включен.

---

## 👤 ШАГ 5: Создание суперпользователя

После того как деплой завершен ("Live" статус):

### 5.1 Откройте Render Shell

На страница вашего сервиса: **"Shell"** вкладка

![Shell](https://via.placeholder.com/600x300?text=Open+Shell)

### 5.2 Выполните команду создания админа

```bash
python manage.py createsuperuser
```

**Заполните данные:**
- Username: `admin`
- Email: `admin@example.com`
- Password: `ваш-надежный-пароль`

```
Username: admin
Email: admin@example.com
Password: 
Confirm password: 
Superuser created successfully.
```

---

## 🎉 ШАГ 6: Проверка что всё работает

### Откройте ваш сайт

После деплоя Render даст вам URL вида:

```
https://lms-xxxxx.onrender.com
```

### Проверьте:

1. **Главная страница** → `https://lms-xxxxx.onrender.com`
   - Должна загружаться без ошибок

2. **Админ панель** → `https://lms-xxxxx.onrender.com/admin`
   - Войдите с admin / ваш-пароль
   - Проверьте что работают все таблицы

3. **Логин обычного пользователя** → `https://lms-xxxxx.onrender.com/login`
   - Попробуйте залогиниться

4. **Курсы и видео** 
   - Загрузится ли страница курса
   - Загрузится ли YouTube видео

---

## 🔗 Полезные ссылки после деплоя

```
Production URL:    https://lms-xxxxx.onrender.com
Admin Panel:       https://lms-xxxxx.onrender.com/admin
GitHub Repo:       https://github.com/YOUR_USERNAME/lms
Supabase Console:  https://app.supabase.com
Render Dashboard:  https://dashboard.render.com
```

---

## 🆘 Решение проблем

### Проблема: "502 Bad Gateway"

**Причины:**
- Приложение не запустилось
- Ошибка в коде Python
- Недостаточно памяти (free tier ограничение)

**Решение:**
1. Откройте Shell на Render
2. Запустите миграции вручную: `python manage.py migrate`
3. Проверьте логи: кликните на сервис → "Logs"

### Проблема: "Error: connect ECONNREFUSED"

**Это ошибка подключения к БД.**

Проверьте:
1. DATABASE_URL скопирована правильно
2. Supabase база доступна (Project Settings → Database → Connection string)
3. Добавьте SSL сертификат: `?sslmode=require` в конце URL

### Проблема: "ModuleNotFoundError: No module named 'django'"

**Решение:**
Render не установил зависимости. Проверьте:
1. `requirements.txt` в корне проекта
2. Выполните пересоздание сервиса (нажмите "Manual Deploy" на Render)

### Проблема: "Static files not loading"

**Решение:**
```bash
# В Render Shell
python manage.py collectstatic --noinput
```

---

## 📊 После успешного деплоя

### Рекомендации:

1. **Отключите DEBUG режим** (уже сделано в конфиге)
2. **Используйте надежный пароль** для админа
3. **Регулярно проверяйте логи** на ошибки
4. **Делайте резервные копии Supabase** базы данных
5. **Обновляйте dependencies** регулярно

---

## 🚀 Быстрая переразвёртка (если нужно переделать)

Если что-то пошло не так, можно всё пересоздать:

1. На Render: удалите сервис
2. На GitHub: убедитесь что код обновлен
3. На Render: создайте новый Web Service (повторите шаги 3-4)

---

**Статус:** ✅ Платформа готова  
**Следующий шаг:** Пройдите шаги 1-6 выше  
**Время:** ~15 минут

Если что-то не ясно, проверьте **DEPLOYMENT.md** для подробной информации.
