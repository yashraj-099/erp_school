import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'school_erp.settings')
django.setup()

from core.models import User

for username in ['admin', 'teacher', 'student']:
    try:
        u = User.objects.get(username=username)
        u.set_password('password')
        u.save()
        print(f'{username} password set to password')
    except User.DoesNotExist:
        print(f'User {username} does not exist')
