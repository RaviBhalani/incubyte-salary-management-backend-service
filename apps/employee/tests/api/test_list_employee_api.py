import pytest
from rest_framework import status

from apps.employee.tests.constants import (
    COUNT_KEY,
    DATA_KEY,
    EMPLOYEE_ID_FIELD,
    JOB_TITLE_FIELD,
    OTHER_EMPLOYEE_DEPARTMENT,
    OTHER_EMPLOYEE_EMAIL,
    OTHER_EMPLOYEE_ID,
    OTHER_EMPLOYEE_JOB_TITLE,
    OTHER_EMPLOYEE_NAME,
    RESULTS_KEY,
    TEST_EMPLOYEE_JOB_TITLE,
)
from apps.employee.tests.factories import create_employee
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

    def test_returns_only_employees_matching_job_title_filter(self, authenticated_client, employee_url, employee):
        create_employee(
            employee_id=OTHER_EMPLOYEE_ID,
            name=OTHER_EMPLOYEE_NAME,
            email=OTHER_EMPLOYEE_EMAIL,
            job_title=OTHER_EMPLOYEE_JOB_TITLE,
            department=OTHER_EMPLOYEE_DEPARTMENT,
        )

        response = authenticated_client.get(f"{employee_url}?job_title={TEST_EMPLOYEE_JOB_TITLE}", format=JSON_FORMAT)
        results = response.data[DATA_KEY]

        assert response.status_code == status.HTTP_200_OK
        assert len(results) > 0
        assert all(e[JOB_TITLE_FIELD] == TEST_EMPLOYEE_JOB_TITLE for e in results)

    def test_returns_paginated_results_when_page_param_is_provided(self, authenticated_client, employee_url, employee):
        response = authenticated_client.get(f"{employee_url}?page=1", format=JSON_FORMAT)
        data = response.data[DATA_KEY]
        employee_ids = [e[EMPLOYEE_ID_FIELD] for e in data[RESULTS_KEY]]

        assert response.status_code == status.HTTP_200_OK
        assert COUNT_KEY in data
        assert RESULTS_KEY in data
        assert employee.employee_id in employee_ids
