from django.db.models import IntegerField, Max
from django.db.models.functions import Cast, Substr
from rest_framework.serializers import ModelSerializer, ValidationError

from apps.employee.constants import (
    COMPANY_EMAIL_DOMAIN,
    EMPLOYEE_EMAIL_PREFIX,
    EMPLOYEE_ID_PREFIX,
    INVALID_JOB_TITLE_DEPARTMENT_MESSAGE,
    JOB_TITLE_DEPARTMENT_MAP,
)
from apps.employee.models import Employee


class EmployeeWriteSerializer(ModelSerializer):

    class Meta:
        model = Employee
        fields = "__all__"
        read_only_fields = ["employee_id", "email"]

    @staticmethod
    def _validate_job_title_department(job_title, department):
        if JOB_TITLE_DEPARTMENT_MAP.get(job_title) != department:
            raise ValidationError({"department": INVALID_JOB_TITLE_DEPARTMENT_MESSAGE})


class EmployeeCreateSerializer(EmployeeWriteSerializer):

    class Meta(EmployeeWriteSerializer.Meta):
        read_only_fields = [*EmployeeWriteSerializer.Meta.read_only_fields, "is_active"]

    def validate(self, data):
        self._validate_job_title_department(data.get("job_title"), data.get("department"))
        return data

    @staticmethod
    def _get_next_employee_number():
        max_num = Employee.objects.aggregate(
            max_num=Max(Cast(Substr("employee_id", 4), IntegerField()))
        )["max_num"] or 0
        return max_num + 1

    def create(self, validated_data):
        next_num = self._get_next_employee_number()
        validated_data["employee_id"] = f"{EMPLOYEE_ID_PREFIX}{next_num}"
        validated_data["email"] = f"{EMPLOYEE_EMAIL_PREFIX}_{next_num}@{COMPANY_EMAIL_DOMAIN}"
        return super().create(validated_data)


class EmployeeUpdateSerializer(EmployeeWriteSerializer):

    def validate(self, data):
        job_title = data.get("job_title", self.instance.job_title)
        department = data.get("department", self.instance.department)
        self._validate_job_title_department(job_title, department)
        return data
