import json
import django
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "horilla.settings")
django.setup()

from django.contrib.auth.models import User
from employee.models import Employee

with open("local_data.json") as f:
    data = json.load(f)

created = 0

for obj in data:
    if obj["model"] == "employee.employee":
        fields = obj["fields"]

        try:
            user = User.objects.get(pk=fields["employee_user_id"])
        except User.DoesNotExist:
            continue

        emp, _ = Employee.objects.get_or_create(
            employee_user_id=user,
            defaults={
                "employee_first_name": fields.get("employee_first_name", ""),
                "employee_last_name": fields.get("employee_last_name", ""),
                "email": fields.get("email", ""),
                "is_active": True,
            },
        )

        emp.is_active = True
        emp.save()
        created += 1

print(f"Employees restored: {created}")

