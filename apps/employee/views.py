from apps.core.constants import GET, PATCH, POST
from apps.core.views import BaseViewset
from apps.employee.models import Employee
from apps.employee.serializers import EmployeeSerializer


class EmployeeViewSet(BaseViewset):
    http_method_names = [GET, POST, PATCH]
    serializer_class = EmployeeSerializer
    queryset = Employee.objects.all()
