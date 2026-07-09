release: python manage.py migrate --noinput && python manage.py ensure_superuser
web: gunicorn backend.wsgi --log-file -
