import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "horilla.settings")
django.setup()

from django.contrib.auth.models import User
from employee.models import Employee

created = 0
existing = 0

for user in User.objects.all():
    emp, was_created = Employee.objects.get_or_create(
        employee_user_id=user,
        defaults={
            "employee_first_name": user.first_name or user.username,
            "employee_last_name": user.last_name or "",
            "email": user.email,
            "is_active": True,
        },
    )

    if was_created:
        created += 1
    else:
        existing += 1

    emp.is_active = True
    emp.save()

print(f"Employees created: {created}")
print(f"Employees already existed: {existing}")

