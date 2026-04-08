import pytest
from rest_framework import status

from apps.employee.tests.constants import (
    COUNT_KEY,
    COUNTRY_FIELD,
    DATA_KEY,
    DEPARTMENT_FIELD,
    EMAIL_FIELD,
    EMPLOYEE_EMAIL_SEARCH_QUERY,
    EMPLOYEE_ID_FIELD,
    EMPLOYEE_ID_SEARCH_QUERY,
    EMPLOYEE_SEARCH_QUERY,
    JOB_TITLE_FIELD,
    NAME_FIELD,
    RESULTS_KEY,
    SALARY_FIELD,
    TEST_EMPLOYEE_COUNTRY,
    TEST_EMPLOYEE_DEPARTMENT,
    TEST_EMPLOYEE_JOB_TITLE,
    TEST_EMPLOYEE_SALARY,
)
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

    def test_returns_only_employees_matching_job_title_filter(
            self,
            authenticated_client,
            employee_url,
            employee,
            other_employee
    ):
        response = authenticated_client.get(f"{employee_url}?job_title={TEST_EMPLOYEE_JOB_TITLE}", format=JSON_FORMAT)
        results = response.data[DATA_KEY]

        assert response.status_code == status.HTTP_200_OK
        assert len(results) > 0
        assert all(e[JOB_TITLE_FIELD] == TEST_EMPLOYEE_JOB_TITLE for e in results)

    def test_returns_only_employees_matching_department_filter(
            self,
            authenticated_client,
            employee_url,
            employee,
            other_employee
    ):
        response = authenticated_client.get(f"{employee_url}?department={TEST_EMPLOYEE_DEPARTMENT}", format=JSON_FORMAT)
        results = response.data[DATA_KEY]

        assert response.status_code == status.HTTP_200_OK
        assert len(results) > 0
        assert all(e[DEPARTMENT_FIELD] == TEST_EMPLOYEE_DEPARTMENT for e in results)

    def test_returns_only_employees_matching_country_filter(
            self,
            authenticated_client,
            employee_url,
            employee,
            other_employee
    ):
        response = authenticated_client.get(f"{employee_url}?country={TEST_EMPLOYEE_COUNTRY}", format=JSON_FORMAT)
        results = response.data[DATA_KEY]

        assert response.status_code == status.HTTP_200_OK
        assert len(results) > 0
        assert all(e[COUNTRY_FIELD] == TEST_EMPLOYEE_COUNTRY for e in results)

    def test_returns_only_employees_within_salary_range_filter(
            self,
            authenticated_client,
            employee_url,
            employee,
            other_employee
    ):
        response = authenticated_client.get(
            f"{employee_url}?salary_min={TEST_EMPLOYEE_SALARY}&salary_max={TEST_EMPLOYEE_SALARY}",
            format=JSON_FORMAT,
        )
        results = response.data[DATA_KEY]

        assert response.status_code == status.HTTP_200_OK
        assert len(results) > 0
        assert all(e[SALARY_FIELD] == TEST_EMPLOYEE_SALARY for e in results)

    def test_returns_only_employees_matching_search_query(
            self,
            authenticated_client,
            employee_url,
            employee,
            other_employee
    ):
        response = authenticated_client.get(f"{employee_url}?search={EMPLOYEE_SEARCH_QUERY}", format=JSON_FORMAT)
        results = response.data[DATA_KEY]

        assert response.status_code == status.HTTP_200_OK
        assert len(results) > 0
        assert all(EMPLOYEE_SEARCH_QUERY.lower() in e[NAME_FIELD].lower() for e in results)

    def test_returns_only_employees_matching_search_query_by_email(
            self,
            authenticated_client,
            employee_url,
            employee,
            other_employee
    ):
        response = authenticated_client.get(f"{employee_url}?search={EMPLOYEE_EMAIL_SEARCH_QUERY}", format=JSON_FORMAT)
        results = response.data[DATA_KEY]

        assert response.status_code == status.HTTP_200_OK
        assert len(results) > 0
        assert all(EMPLOYEE_EMAIL_SEARCH_QUERY.lower() in e[EMAIL_FIELD].lower() for e in results)

    def test_returns_only_employees_matching_search_query_by_employee_id(
            self,
            authenticated_client,
            employee_url,
            employee,
            other_employee
    ):
        response = authenticated_client.get(f"{employee_url}?search={EMPLOYEE_ID_SEARCH_QUERY}", format=JSON_FORMAT)
        results = response.data[DATA_KEY]

        assert response.status_code == status.HTTP_200_OK
        assert len(results) > 0
        assert all(EMPLOYEE_ID_SEARCH_QUERY.lower() in e[EMPLOYEE_ID_FIELD].lower() for e in results)

    def test_returns_paginated_results_when_page_param_is_provided(self, authenticated_client, employee_url, employee):
        response = authenticated_client.get(f"{employee_url}?page=1", format=JSON_FORMAT)
        data = response.data[DATA_KEY]
        employee_ids = [e[EMPLOYEE_ID_FIELD] for e in data[RESULTS_KEY]]

        assert response.status_code == status.HTTP_200_OK
        assert COUNT_KEY in data
        assert RESULTS_KEY in data
        assert employee.employee_id in employee_ids
