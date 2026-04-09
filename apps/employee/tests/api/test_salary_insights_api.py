import pytest
from rest_framework import status

from apps.employee.tests.constants import (
    AVG_SALARY_FIELD,
    COUNTRY_FIELD,
    DATA_KEY,
    DEPARTMENT_FIELD,
    JOB_TITLE_FIELD,
    MAX_SALARY_FIELD,
    MIN_SALARY_FIELD,
    OTHER_EMPLOYEE_SALARY,
    SALARY_MAX_QUERY_PARAM,
    SALARY_MIN_QUERY_PARAM,
    TEST_EMPLOYEE_COUNTRY,
    TEST_EMPLOYEE_DEPARTMENT,
    TEST_EMPLOYEE_JOB_TITLE,
    TEST_EMPLOYEE_SALARY,
    TOTAL_EMPLOYEES_FIELD,
)
from tests.constants import JSON_FORMAT

pytestmark = pytest.mark.django_db


class TestSalaryInsightsApi:

    def test_returns_all_metrics_for_all_active_employees(
        self, authenticated_client, salary_insights_url, employee, other_employee
    ):
        response = authenticated_client.get(salary_insights_url, format=JSON_FORMAT)
        data = response.data[DATA_KEY]

        assert response.status_code == status.HTTP_200_OK
        assert data[MIN_SALARY_FIELD] == min(TEST_EMPLOYEE_SALARY, OTHER_EMPLOYEE_SALARY)
        assert data[MAX_SALARY_FIELD] == max(TEST_EMPLOYEE_SALARY, OTHER_EMPLOYEE_SALARY)
        assert data[AVG_SALARY_FIELD] == round((TEST_EMPLOYEE_SALARY + OTHER_EMPLOYEE_SALARY) / 2)
        assert data[TOTAL_EMPLOYEES_FIELD] == 2

    def test_returns_metrics_filtered_by_job_title(
        self, authenticated_client, salary_insights_url, employee, other_employee
    ):
        response = authenticated_client.get(
            f"{salary_insights_url}?{JOB_TITLE_FIELD}={TEST_EMPLOYEE_JOB_TITLE}",
            format=JSON_FORMAT,
        )
        data = response.data[DATA_KEY]

        assert response.status_code == status.HTTP_200_OK
        assert data[TOTAL_EMPLOYEES_FIELD] == 1
        assert data[MIN_SALARY_FIELD] == TEST_EMPLOYEE_SALARY
        assert data[MAX_SALARY_FIELD] == TEST_EMPLOYEE_SALARY
        assert data[AVG_SALARY_FIELD] == TEST_EMPLOYEE_SALARY

    def test_returns_metrics_filtered_by_department(
        self, authenticated_client, salary_insights_url, employee, other_employee
    ):
        response = authenticated_client.get(
            f"{salary_insights_url}?{DEPARTMENT_FIELD}={TEST_EMPLOYEE_DEPARTMENT}",
            format=JSON_FORMAT,
        )
        data = response.data[DATA_KEY]

        assert response.status_code == status.HTTP_200_OK
        assert data[TOTAL_EMPLOYEES_FIELD] == 1
        assert data[MIN_SALARY_FIELD] == TEST_EMPLOYEE_SALARY
        assert data[MAX_SALARY_FIELD] == TEST_EMPLOYEE_SALARY
        assert data[AVG_SALARY_FIELD] == TEST_EMPLOYEE_SALARY

    def test_returns_metrics_filtered_by_country(
        self, authenticated_client, salary_insights_url, employee, other_employee
    ):
        response = authenticated_client.get(
            f"{salary_insights_url}?{COUNTRY_FIELD}={TEST_EMPLOYEE_COUNTRY}",
            format=JSON_FORMAT,
        )
        data = response.data[DATA_KEY]

        assert response.status_code == status.HTTP_200_OK
        assert data[TOTAL_EMPLOYEES_FIELD] == 1
        assert data[MIN_SALARY_FIELD] == TEST_EMPLOYEE_SALARY
        assert data[MAX_SALARY_FIELD] == TEST_EMPLOYEE_SALARY
        assert data[AVG_SALARY_FIELD] == TEST_EMPLOYEE_SALARY

    def test_returns_metrics_filtered_by_minimum_salary(
        self, authenticated_client, salary_insights_url, employee, other_employee
    ):
        response = authenticated_client.get(
            f"{salary_insights_url}?{SALARY_MIN_QUERY_PARAM}={OTHER_EMPLOYEE_SALARY}",
            format=JSON_FORMAT,
        )
        data = response.data[DATA_KEY]

        assert response.status_code == status.HTTP_200_OK
        assert data[TOTAL_EMPLOYEES_FIELD] == 1
        assert data[MIN_SALARY_FIELD] == OTHER_EMPLOYEE_SALARY
        assert data[MAX_SALARY_FIELD] == OTHER_EMPLOYEE_SALARY
        assert data[AVG_SALARY_FIELD] == OTHER_EMPLOYEE_SALARY

    def test_returns_metrics_filtered_by_maximum_salary(
        self, authenticated_client, salary_insights_url, employee, other_employee
    ):
        response = authenticated_client.get(
            f"{salary_insights_url}?{SALARY_MAX_QUERY_PARAM}={TEST_EMPLOYEE_SALARY}",
            format=JSON_FORMAT,
        )
        data = response.data[DATA_KEY]

        assert response.status_code == status.HTTP_200_OK
        assert data[TOTAL_EMPLOYEES_FIELD] == 1
        assert data[MIN_SALARY_FIELD] == TEST_EMPLOYEE_SALARY
        assert data[MAX_SALARY_FIELD] == TEST_EMPLOYEE_SALARY
        assert data[AVG_SALARY_FIELD] == TEST_EMPLOYEE_SALARY

    def test_returns_metrics_filtered_by_salary_range(
        self, authenticated_client, salary_insights_url, employee, other_employee
    ):
        response = authenticated_client.get(
            f"{salary_insights_url}?"
            f"{SALARY_MIN_QUERY_PARAM}={TEST_EMPLOYEE_SALARY}&"
            f"{SALARY_MAX_QUERY_PARAM}={TEST_EMPLOYEE_SALARY}",
            format=JSON_FORMAT,
        )
        data = response.data[DATA_KEY]

        assert response.status_code == status.HTTP_200_OK
        assert data[TOTAL_EMPLOYEES_FIELD] == 1
        assert data[MIN_SALARY_FIELD] == TEST_EMPLOYEE_SALARY
        assert data[MAX_SALARY_FIELD] == TEST_EMPLOYEE_SALARY
        assert data[AVG_SALARY_FIELD] == TEST_EMPLOYEE_SALARY

    def test_returns_metrics_with_all_filters_applied(
        self, authenticated_client, salary_insights_url, employee, other_employee
    ):
        response = authenticated_client.get(
            f"{salary_insights_url}?"
            f"{COUNTRY_FIELD}={TEST_EMPLOYEE_COUNTRY}&"
            f"{JOB_TITLE_FIELD}={TEST_EMPLOYEE_JOB_TITLE}&"
            f"{DEPARTMENT_FIELD}={TEST_EMPLOYEE_DEPARTMENT}&"
            f"{SALARY_MIN_QUERY_PARAM}={TEST_EMPLOYEE_SALARY}&"
            f"{SALARY_MAX_QUERY_PARAM}={TEST_EMPLOYEE_SALARY}",
            format=JSON_FORMAT,
        )
        data = response.data[DATA_KEY]

        assert response.status_code == status.HTTP_200_OK
        assert data[TOTAL_EMPLOYEES_FIELD] == 1
        assert data[MIN_SALARY_FIELD] == TEST_EMPLOYEE_SALARY
        assert data[MAX_SALARY_FIELD] == TEST_EMPLOYEE_SALARY
        assert data[AVG_SALARY_FIELD] == TEST_EMPLOYEE_SALARY
