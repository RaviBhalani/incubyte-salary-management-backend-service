import pytest
from rest_framework import status

from apps.employee.tests.constants import DATA_KEY, EMAIL_FIELD, EMPLOYEE_ID_FIELD
from tests.constants import JSON_FORMAT

pytestmark = pytest.mark.django_db


class TestRetrieveEmployeeApi:

    def test_returns_employee_by_id(self, authenticated_client, employee_detail_url, employee):
        response = authenticated_client.get(employee_detail_url, format=JSON_FORMAT)

        assert response.status_code == status.HTTP_200_OK
        assert response.data[DATA_KEY][EMPLOYEE_ID_FIELD] == employee.employee_id
        assert response.data[DATA_KEY][EMAIL_FIELD] == employee.email
