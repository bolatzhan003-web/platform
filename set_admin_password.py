import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lms.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()
user = User.objects.get(username='admin')
user.set_password('admin123')
user.save()

print('Password set successfully for admin user')
print('  Username: admin')
print('  Password: admin123')
