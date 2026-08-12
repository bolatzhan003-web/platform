FROM python:3.12-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y gcc g++ && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt gunicorn

# Copy project
COPY . .

# Create directories
RUN mkdir -p staticfiles media logs

# Collect static
RUN python manage.py collectstatic --noinput --clear 2>&1 || true

# Run migrations
RUN python manage.py migrate --noinput 2>&1 || true

EXPOSE 8000

# Simple start command
CMD exec gunicorn lms.wsgi:application --bind 0.0.0.0:8000 --workers 4 --timeout 120 --access-logfile - --error-logfile -
