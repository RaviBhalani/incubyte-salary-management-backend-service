from apps.core.constants import CREATE, GET, PATCH, POST
from apps.core.views import BaseViewset
from apps.employee.models import Employee
from apps.employee.serializers import EmployeeCreateSerializer, EmployeeUpdateSerializer


class EmployeeViewSet(BaseViewset):
    http_method_names = [GET, POST, PATCH]
    queryset = Employee.objects.filter(is_active=True)

    def get_serializer_class(self):
        if self.action == CREATE:
            return EmployeeCreateSerializer
        return EmployeeUpdateSerializer
