import pytest
from rest_framework import status

from apps.employee.tests.constants import COUNT_KEY, DATA_KEY, EMPLOYEE_ID_FIELD, RESULTS_KEY
from tests.constants import JSON_FORMAT

pytestmark = pytest.mark.django_db


class TestListEmployeeApi:

    def test_returns_list_of_employees(self, authenticated_client, employee_url, employee):
        response = authenticated_client.get(employee_url, format=JSON_FORMAT)
        employee_ids = [e[EMPLOYEE_ID_FIELD] for e in response.data[DATA_KEY]]

        assert response.status_code == status.HTTP_200_OK
        assert employee.employee_id in employee_ids

    def test_excludes_deleted_employees(self, authenticated_client, employee_url, deleted_employee):
        response = authenticated_client.get(employee_url, format=JSON_FORMAT)
        employee_ids = [e[EMPLOYEE_ID_FIELD] for e in response.data[DATA_KEY]]

        assert response.status_code == status.HTTP_200_OK
        assert deleted_employee.employee_id not in employee_ids

    def test_returns_paginated_results_when_page_param_is_provided(self, authenticated_client, employee_url, employee):
        response = authenticated_client.get(f"{employee_url}?page=1", format=JSON_FORMAT)
        data = response.data[DATA_KEY]
        employee_ids = [e[EMPLOYEE_ID_FIELD] for e in data[RESULTS_KEY]]

        assert response.status_code == status.HTTP_200_OK
        assert COUNT_KEY in data
        assert RESULTS_KEY in data
        assert employee.employee_id in employee_ids
