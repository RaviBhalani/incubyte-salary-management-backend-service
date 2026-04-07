import pytest
from rest_framework import status

from apps.employee.tests.constants import DATA_KEY
from tests.constants import JSON_FORMAT

pytestmark = pytest.mark.django_db


class TestListEmployeeApi:

    def test_returns_list_of_employees(self, authenticated_client, employee_url, employee):
        response = authenticated_client.get(employee_url, format=JSON_FORMAT)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data[DATA_KEY]) > 0
