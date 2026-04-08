import django_filters

from apps.employee.models import Employee


class EmployeeFilter(django_filters.FilterSet):
    class Meta:
        model = Employee
        fields = ["job_title", "department"]
