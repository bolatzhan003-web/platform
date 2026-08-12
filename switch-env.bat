@echo off
REM Скрипт для быстрого переключения между локальным и production окружением (Windows)

if "%1"=="local" (
    echo Switching to LOCAL development environment SQLite...
    copy /Y .env.local .env
    echo ✓ Environment set to LOCAL
    echo   Database: SQLite db.sqlite3
    echo   Debug: True
    echo.
    echo Run: python manage.py runserver
    goto :eof
)

if "%1"=="prod" (
    echo Switching to PRODUCTION environment Supabase PostgreSQL...
    copy /Y .env.production .env
    echo ✓ Environment set to PRODUCTION
    echo   Database: Supabase PostgreSQL
    echo   Debug: False
    echo.
    echo WARNING: Update DJANGO_SECRET_KEY in .env before deploying!
    echo Run: python manage.py migrate
    goto :eof
)

if "%1"=="production" (
    echo Switching to PRODUCTION environment Supabase PostgreSQL...
    copy /Y .env.production .env
    echo ✓ Environment set to PRODUCTION
    echo   Database: Supabase PostgreSQL
    echo   Debug: False
    echo.
    echo WARNING: Update DJANGO_SECRET_KEY in .env before deploying!
    echo Run: python manage.py migrate
    goto :eof
)

echo Usage: switch-env.bat [local^|prod]
echo.
echo Examples:
echo   switch-env.bat local   - Switch to local development SQLite
echo   switch-env.bat prod    - Switch to production PostgreSQL
