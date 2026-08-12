release: python manage.py migrate --noinput 2>/dev/null || true; python manage.py collectstatic --noinput 2>/dev/null || true
web: gunicorn lms.wsgi:application --bind 0.0.0.0:3000 --workers 2 --timeout 120
