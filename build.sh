#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt

python manage.py migrate --noinput
python manage.py collectstatic --noinput
echo "from django.contrib.auth.models import User; \
User.objects.filter(username='admin').exists() or \
User.objects.create_superuser('admin','admin@test.com','Admin@123')" | python manage.py shell
