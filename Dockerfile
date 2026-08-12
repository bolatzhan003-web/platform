FROM python:3.12-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . .

# Create staticfiles directory
RUN mkdir -p staticfiles

# Collect static files
RUN python manage.py collectstatic --noinput || true

# Run migrations
RUN python manage.py migrate || true

# Expose port
EXPOSE 8000

# Start gunicorn
CMD ["gunicorn", "lms.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "2", "--timeout", "120"]
