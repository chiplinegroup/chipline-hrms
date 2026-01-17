#!/bin/sh
set -e

echo "Running migrations..."
python manage.py migrate --noinput

echo "Loading local data (if present)..."
python manage.py loaddata local_data.json || echo "⚠️ Data already loaded or skipped"

echo "Ensuring admin + employee..."
python render_setup.py

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Starting Gunicorn..."
exec gunicorn horilla.wsgi:application --bind 0.0.0.0:$PORT

