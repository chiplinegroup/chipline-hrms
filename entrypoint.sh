#!/bin/sh
set -e

python manage.py migrate

# Load initial data ONLY if DB is empty
python - <<EOF
from base.models import Company
if not Company.objects.exists():
    print("Loading initial data.json")
    import os
    os.system("python manage.py loaddata data.json")
else:
    print("Skipping data.json (already loaded)")
EOF

python render_setup.py || true

gunicorn horilla.wsgi:application --bind 0.0.0.0:$PORT

