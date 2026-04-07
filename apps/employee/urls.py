from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apps.employee.constants import EMPLOYEE_BASENAME, EMPLOYEE_URL
from apps.employee.views import EmployeeViewset

router = DefaultRouter()
router.register(EMPLOYEE_URL, EmployeeViewset, basename=EMPLOYEE_BASENAME)

urlpatterns = [
    path("", include(router.urls)),
]
