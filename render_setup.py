import os
import django

# Tell Django where settings are
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "horilla.settings")
django.setup()

from django.contrib.auth.models import User
from employee.models import Employee

# Admin credentials
USERNAME = "chipline"
EMAIL = "ceo.chipline@gmail.com"
PASSWORD = os.environ.get("ADMIN_PASSWORD", "ChangeMe123!")

# 1️⃣ Create admin user if not exists
user, created = User.objects.get_or_create(
    username=USERNAME,
    defaults={
        "email": EMAIL,
        "is_staff": True,
        "is_superuser": True,
    },
)

if created:
    user.set_password(PASSWORD)
    user.save()
    print("Admin user created")
else:
    print("Admin user already exists")

# 2️⃣ Create employee linked to admin user
if not Employee.objects.filter(employee_user_id=user).exists():
    Employee.objects.create(
        employee_user_id=user,
        employee_first_name="Admin",
        employee_last_name="User",
        email=EMAIL,
        is_active=True,
    )
    print("Employee created for admin")
else:
    print("Employee already exists")

