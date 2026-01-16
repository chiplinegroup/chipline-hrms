#!/bin/sh
set -e

echo "Making migrations (if missing)..."
python manage.py makemigrations --noinput

echo "Running migrations (force syncdb)..."
python manage.py migrate --noinput --run-syncdb

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Starting Gunicorn..."
gunicorn horilla.wsgi:application --bind 0.0.0.0:$PORT

