from rest_framework.serializers import ModelSerializer, ValidationError

from apps.employee.constants import (
    INVALID_JOB_TITLE_DEPARTMENT_MESSAGE,
    JOB_TITLE_DEPARTMENT_MAP,
)
from apps.employee.models import Employee


class EmployeeSerializer(ModelSerializer):

    class Meta:
        model = Employee
        fields = "__all__"

    def validate(self, data):
        job_title = data.get("job_title")
        department = data.get("department")

        if job_title and department:
            if JOB_TITLE_DEPARTMENT_MAP.get(job_title) != department:
                raise ValidationError({"department": INVALID_JOB_TITLE_DEPARTMENT_MESSAGE})
        return data
