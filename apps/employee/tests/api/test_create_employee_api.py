import pytest
from rest_framework import status

from apps.employee.tests.constants import DATA_KEY, EMAIL_FIELD, EMPLOYEE_ID_FIELD
from tests.constants import JSON_FORMAT

pytestmark = pytest.mark.django_db


class TestCreateEmployeeApi:

    def test_creates_employee_with_valid_data(self, authenticated_client, employee_url, employee_payload):
        response = authenticated_client.post(employee_url, employee_payload, format=JSON_FORMAT)

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data[DATA_KEY][EMPLOYEE_ID_FIELD] == employee_payload[EMPLOYEE_ID_FIELD]
        assert response.data[DATA_KEY][EMAIL_FIELD] == employee_payload[EMAIL_FIELD]
