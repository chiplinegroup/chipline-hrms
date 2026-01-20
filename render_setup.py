import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "horilla.settings")
django.setup()

from django.contrib.auth.models import User
from employee.models import Employee

USERNAME = "chipline"
EMAIL = "ceo.chipline@gmail.com"
PASSWORD = os.environ.get("ADMIN_PASSWORD", "ChangeMe123!")

# 1️⃣ FORCE create or update admin user
user, _ = User.objects.get_or_create(username=USERNAME)
user.email = EMAIL
user.is_staff = True
user.is_superuser = True
user.set_password(PASSWORD)   # 🔥 FORCE password reset
user.save()

print("Admin user ensured & password reset")

# 2️⃣ FORCE create or update employee
emp, _ = Employee.objects.get_or_create(
    employee_user_id=user,
    defaults={
        "employee_first_name": "Admin",
        "employee_last_name": "User",
        "email": EMAIL,
        "is_active": True,
    },
)

emp.is_active = True
emp.email = EMAIL
emp.is_active = True
emp.email = EMAIL

# 🔒 Skip full_clean to avoid file validation errors on Render
Employee.objects.filter(pk=emp.pk).update(
    is_active=True,
    email=EMAIL
)

print("Employee ensured & active")

from employee.models import Employee

print("EMPLOYEE COUNT =", Employee.objects.count())

