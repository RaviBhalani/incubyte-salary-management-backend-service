import pytest
from rest_framework import status

from apps.employee.tests.constants import (
    DATA_KEY,
    NAME_FIELD,
    UPDATED_EMPLOYEE_NAME,
    UPDATED_EMPLOYEE_SALARY,
    SALARY_FIELD
)
from tests.constants import JSON_FORMAT

pytestmark = pytest.mark.django_db


class TestUpdateEmployeeApi:

    def test_updates_employee_with_valid_data(self, authenticated_client, employee_detail_url, employee):
        response = authenticated_client.patch(
            employee_detail_url,
            {NAME_FIELD: UPDATED_EMPLOYEE_NAME, SALARY_FIELD: UPDATED_EMPLOYEE_SALARY},
            format=JSON_FORMAT,
        )

        assert response.status_code == status.HTTP_200_OK
        assert response.data[DATA_KEY][NAME_FIELD] == UPDATED_EMPLOYEE_NAME
