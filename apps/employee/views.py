from apps.core.views import BaseViewset
from apps.employee.models import Employee
from apps.employee.serializers import EmployeeSerializer


class EmployeeViewset(BaseViewset):
    serializer_class = EmployeeSerializer
    queryset = Employee.objects.all()
