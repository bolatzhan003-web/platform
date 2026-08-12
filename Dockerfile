FROM python:3.13-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y gcc g++ && rm -rf /var/lib/apt/lists/*

# Copy and install requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt gunicorn

# Copy entire project
COPY . .

# Create staticfiles directory
RUN mkdir -p staticfiles media

# Collect static files
RUN python manage.py collectstatic --noinput --clear

# Run migrations
RUN python manage.py migrate --noinput || true

# Expose port
EXPOSE 8000

# Start server
CMD ["gunicorn", "lms.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "2", "--timeout", "120"]
