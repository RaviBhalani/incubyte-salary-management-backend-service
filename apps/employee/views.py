from django.db.models import Avg, Count, Max, Min
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter

from apps.core.constants import CREATE, GET, PATCH, POST
from apps.core.custom_exception_handlers import get_response
from apps.core.views import BaseViewset
from apps.employee.constants import SALARY_INSIGHTS_URL_NAME, SALARY_INSIGHTS_URL_PATH
from apps.employee.filters import EmployeeFilter
from apps.employee.models import Employee
from apps.employee.serializers import EmployeeCreateSerializer, EmployeeUpdateSerializer


class EmployeeViewSet(BaseViewset):
    http_method_names = [GET, POST, PATCH]
    queryset = Employee.objects.filter(is_active=True)
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_class = EmployeeFilter
    search_fields = ["employee_id", "name", "email"]

    def get_serializer_class(self):
        if self.action == CREATE:
            return EmployeeCreateSerializer
        return EmployeeUpdateSerializer

    @action(detail=False, methods=[GET], url_path=SALARY_INSIGHTS_URL_PATH, url_name=SALARY_INSIGHTS_URL_NAME)
    def salary_insights(self, request):
        queryset = self.filter_queryset(self.get_queryset())
        aggregation = queryset.aggregate(
            min_salary=Min("salary"),
            max_salary=Max("salary"),
            avg_salary=Avg("salary"),
            total_employees=Count("id"),
        )
        avg = aggregation["avg_salary"]
        aggregation["avg_salary"] = round(avg) if avg is not None else None
        return get_response(data=aggregation, success=True)
