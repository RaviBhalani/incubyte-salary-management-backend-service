from django.apps import AppConfig

from apps.employee.constants import EMPLOYEE_APP


class EmployeeConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = EMPLOYEE_APP
