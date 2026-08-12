release: python manage.py migrate && python manage.py collectstatic --noinput
web: gunicorn lms.wsgi:application --bind 0.0.0.0:3000 --workers 2 --timeout 120
