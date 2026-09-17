import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lms.settings')
django.setup()

from django.contrib.auth import get_user_model
User = get_user_model()

if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
    print("✓ Admin created: admin / admin123")
else:
    print("✓ Admin already exists")

if not User.objects.filter(username='teacher').exists():
    User.objects.create_user(
        username='teacher',
        email='teacher@example.com',
        password='demo123456',
        is_staff=True
    )
    print("✓ Teacher created: teacher / demo123456")
else:
    print("✓ Teacher already exists")