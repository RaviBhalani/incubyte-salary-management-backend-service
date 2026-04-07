import pytest
from rest_framework import status

from tests.constants import JSON_FORMAT

pytestmark = pytest.mark.django_db


class TestDeleteEmployeeApi:

    def test_deletes_employee(self, authenticated_client, employee_detail_url, employee):
        response = authenticated_client.delete(employee_detail_url, format=JSON_FORMAT)

        assert response.status_code == status.HTTP_204_NO_CONTENT
