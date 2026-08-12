# ✅ RENDER DEPLOYMENT CHECKLIST

**Дата:** 2026-08-12  
**Статус:** Готов к деплою  

---

## 🎯 Быстрая инструкция (5 шагов)

### Шаг 1: Подготовка GitHub ✅
- [ ] Код залит в GitHub на ветку `main`
- [ ] Последний коммит пушнут (`git push origin main`)

**Команда если не залили:**
```bash
git init
git add .
git commit -m "Initial: LMS deployment ready"
git remote add origin https://github.com/YOUR_USERNAME/lms.git
git branch -M main
git push -u origin main
```

---

### Шаг 2: Генерируем SECRET_KEY ✅
- [ ] Открыли PowerShell/Terminal
- [ ] Выполнили команду и скопировали результат

**Команда:**
```bash
python -c "import secrets; print(secrets.token_urlsafe(50))"
```

**Результат скопирован:** `_________________________` (вставьте сюда)

---

### Шаг 3: Создание Web Service на Render ✅

#### На render.com:
- [ ] Нажали "+ New"
- [ ] Выбрали "Web Service"
- [ ] Подключили GitHub репозиторий `lms`
- [ ] Заполнили Name: `lms`
- [ ] Выбрали Environment: `Python 3`

#### Build Command:
```bash
pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate
```
- [ ] Скопировали Build Command

#### Start Command:
```bash
gunicorn lms.wsgi:application --bind 0.0.0.0:$PORT --workers 2 --timeout 120
```
- [ ] Скопировали Start Command

---

### Шаг 4: Environment Variables ✅

Добавьте эти переменные в Render (кликните "+ Add Environment Variable"):

```
PYTHON_VERSION = 3.12.10

DJANGO_SECRET_KEY = (ваш ключ из Шага 2)

DJANGO_DEBUG = False

ALLOWED_HOSTS = .onrender.com

DATABASE_URL = postgresql://postgres:29101997.1064sh@db.tugldzcyfvmqogquzvif.supabase.co:5432/postgres?sslmode=require
```

Проверки:
- [ ] PYTHON_VERSION = 3.12.10
- [ ] DJANGO_SECRET_KEY = (новый ключ)
- [ ] DJANGO_DEBUG = False
- [ ] ALLOWED_HOSTS = .onrender.com
- [ ] DATABASE_URL = postgresql://postgres:29101997.1064sh@db.tugldzcyfvmqogquzvif.supabase.co:5432/postgres?sslmode=require

---

### Шаг 5: Нажмите "Create Web Service" ✅

- [ ] Нажали кнопку "Create Web Service"
- [ ] Статус: "Building..." → ожидаем (5-10 минут)
- [ ] Когда статус = "Live" ✅ дальше в Шаг 6

**Мониторинг логов:**
- Зелёные строки = хорошо
- Красные строки = ошибка → читайте ошибку

---

### Шаг 6: Создание суперпользователя ✅

Когда статус "Live":

1. [ ] Открыли Shell вкладку в Render
2. [ ] Выполнили команду:
   ```bash
   python manage.py createsuperuser
   ```
3. [ ] Заполнили:
   - Username: `admin`
   - Email: `admin@example.com`
   - Password: (надежный пароль)
4. [ ] Вышла строка: "Superuser created successfully" ✅

---

### Шаг 7: Проверка работоспособности ✅

Ваш URL будет выглядеть так: `https://lms-xxxxx.onrender.com`

Проверьте:
- [ ] Главная страница загружается
- [ ] Админ панель доступна: `https://lms-xxxxx.onrender.com/admin`
- [ ] Логин работает
- [ ] Курсы видны
- [ ] YouTube видео загружается

---

## 🆘 Если что-то не работает

### Статус: "Build failed" (красные логи)

**Проверьте:**
1. `requirements.txt` в корне папки
2. Python версия 3.12
3. Все зависимости установлены локально

**Решение:** 
```bash
pip install -r requirements.txt
```

---

### Статус: "502 Bad Gateway"

**Проблема:** Приложение не запустилось

**Решение в Shell:**
```bash
python manage.py migrate
python manage.py collectstatic --noinput
```

---

### Ошибка: "could not translate host name db.tugldzcyfvmqogquzvif.supabase.co"

**Проблема:** DATABASE_URL неправильная

**Проверьте:**
- [ ] Скопирована вся строка целиком
- [ ] В конце есть `?sslmode=require`
- [ ] Нет лишних пробелов

**Правильный формат:**
```
postgresql://postgres:29101997.1064sh@db.tugldzcyfvmqogquzvif.supabase.co:5432/postgres?sslmode=require
```

---

### Ошибка: "ModuleNotFoundError: No module named 'django'"

**Решение:**
1. На Render нажмите "Manual Deploy"
2. Дождитесь пересборки

---

## 📊 После успешного деплоя

### Ваши ссылки:
```
🌐 Production:  https://lms-xxxxx.onrender.com
🔧 Admin:       https://lms-xxxxx.onrender.com/admin
📚 Courses:     https://lms-xxxxx.onrender.com/dashboard
```

### Что дальше:
1. Добавьте учебные курсы через админку
2. Пригласите учителей и учеников
3. Загрузьте материалы к урокам
4. Тестируйте YouTube видео

---

## 📝 Итоговый статус

- ✅ Django настроен для production
- ✅ Supabase PostgreSQL подключена
- ✅ Render.yaml готов
- ✅ Все переменные окружения на месте
- 🚀 **ГОТОВО К ДЕПЛОЮ**

---

**Время на деплой:** ~15 минут  
**Сложность:** Низкая (следуйте инструкции шаг за шагом)

После завершения деплоя платформа будет доступна всем в интернете! 🎉
