#!/bin/bash
set -e

python manage.py migrate
python manage.py loaddata local_data.json || true
python render_setup.py
python restore_employees.py
python manage.py collectstatic --noinput

gunicorn horilla.wsgi:application --bind 0.0.0.0:$PORT

