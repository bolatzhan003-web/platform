#!/bin/bash
# Скрипт для быстрого переключения между локальным и production окружением

case "$1" in
  local)
    echo "Switching to LOCAL development environment (SQLite)..."
    cp .env.local .env
    echo "✓ Environment set to LOCAL"
    echo "  Database: SQLite (db.sqlite3)"
    echo "  Debug: True"
    echo ""
    echo "Run: python manage.py runserver"
    ;;

  prod|production)
    echo "Switching to PRODUCTION environment (Supabase PostgreSQL)..."
    cp .env.production .env
    echo "✓ Environment set to PRODUCTION"
    echo "  Database: Supabase PostgreSQL"
    echo "  Debug: False"
    echo ""
    echo "⚠️  IMPORTANT: Update DJANGO_SECRET_KEY in .env before deploying!"
    echo "Run: python manage.py migrate"
    ;;

  *)
    echo "Usage: ./switch-env.sh [local|prod]"
    echo ""
    echo "Examples:"
    echo "  ./switch-env.sh local   - Switch to local development (SQLite)"
    echo "  ./switch-env.sh prod    - Switch to production (PostgreSQL)"
    exit 1
    ;;
esac
