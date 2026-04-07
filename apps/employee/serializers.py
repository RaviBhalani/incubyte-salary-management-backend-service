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


class EmployeeSerializer(ModelSerializer):

    class Meta:
        model = Employee
        fields = "__all__"
        read_only_fields = ["employee_id", "email"]

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

    def validate(self, data):
        instance = self.instance
        job_title = data.get("job_title", instance.job_title if instance else None)
        department = data.get("department", instance.department if instance else None)

        if job_title and department:
            if JOB_TITLE_DEPARTMENT_MAP.get(job_title) != department:
                raise ValidationError({"department": INVALID_JOB_TITLE_DEPARTMENT_MESSAGE})
        return data
