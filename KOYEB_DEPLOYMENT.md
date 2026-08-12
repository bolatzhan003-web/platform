# Koyeb Deployment Guide

## Быстрая инструкция (5 минут)

### 1. Аккаунт
- https://www.koyeb.com → Sign up with GitHub

### 2. Deploy
- Dashboard → "Create Web Service"
- Выберите "GitHub"
- Выберите репо `platform`

### 3. Конфиг
- Service name: `lms`
- Branch: `main`
- Builder: `Buildpack`

### 4. Environment Variables
```
PYTHON_VERSION=3.12
DJANGO_SECRET_KEY=<сгенерируйте новый>
DJANGO_DEBUG=False
ALLOWED_HOSTS=*.koyeb.app,localhost
```

### 5. Port
```
8000
```

### 6. Deploy!
- Нажмите "Deploy"
- Ждите 2-3 минуты
- Получите URL: https://lms-xxxx.koyeb.app

### Логины:
- admin / admin123
- teacher / teacher123
- student / student123

### Регистрация:
- https://lms-xxxx.koyeb.app/register
