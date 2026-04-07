import pytest
from rest_framework import status

from apps.employee.tests.constants import (
    COUNTRY_FIELD,
    DATA_KEY,
    DEPARTMENT_FIELD,
    EMAIL_FIELD,
    EMPLOYEE_ID_FIELD,
    INVALID_COUNTRY,
    INVALID_DEPARTMENT,
    INVALID_JOB_TITLE,
    JOB_TITLE_FIELD,
    MISMATCHED_DEPARTMENT,
    NEGATIVE_SALARY,
    SALARY_ABOVE_MAXIMUM,
    SALARY_BELOW_MINIMUM,
    SALARY_FIELD,
)
from tests.constants import JSON_FORMAT
from tests.helpers.assertions import assert_error_response

pytestmark = pytest.mark.django_db


class TestCreateEmployeeApi:

    def test_creates_employee_with_valid_data(self, authenticated_client, employee_url, employee_payload):
        response = authenticated_client.post(employee_url, employee_payload, format=JSON_FORMAT)

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data[DATA_KEY][EMPLOYEE_ID_FIELD] == employee_payload[EMPLOYEE_ID_FIELD]
        assert response.data[DATA_KEY][EMAIL_FIELD] == employee_payload[EMAIL_FIELD]

    def test_returns_error_for_invalid_job_title(self, authenticated_client, employee_url, employee_payload):
        employee_payload[JOB_TITLE_FIELD] = INVALID_JOB_TITLE
        response = authenticated_client.post(employee_url, employee_payload, format=JSON_FORMAT)

        assert_error_response(response, status.HTTP_400_BAD_REQUEST)

    def test_returns_error_for_invalid_department(self, authenticated_client, employee_url, employee_payload):
        employee_payload[DEPARTMENT_FIELD] = INVALID_DEPARTMENT
        response = authenticated_client.post(employee_url, employee_payload, format=JSON_FORMAT)

        assert_error_response(response, status.HTTP_400_BAD_REQUEST)

    def test_returns_error_for_negative_salary(self, authenticated_client, employee_url, employee_payload):
        employee_payload[SALARY_FIELD] = NEGATIVE_SALARY
        response = authenticated_client.post(employee_url, employee_payload, format=JSON_FORMAT)

        assert_error_response(response, status.HTTP_400_BAD_REQUEST)

    def test_returns_error_for_salary_below_minimum(self, authenticated_client, employee_url, employee_payload):
        employee_payload[SALARY_FIELD] = SALARY_BELOW_MINIMUM
        response = authenticated_client.post(employee_url, employee_payload, format=JSON_FORMAT)

        assert_error_response(response, status.HTTP_400_BAD_REQUEST)

    def test_returns_error_for_salary_above_maximum(self, authenticated_client, employee_url, employee_payload):
        employee_payload[SALARY_FIELD] = SALARY_ABOVE_MAXIMUM
        response = authenticated_client.post(employee_url, employee_payload, format=JSON_FORMAT)

        assert_error_response(response, status.HTTP_400_BAD_REQUEST)

    def test_returns_error_for_invalid_country(self, authenticated_client, employee_url, employee_payload):
        employee_payload[COUNTRY_FIELD] = INVALID_COUNTRY
        response = authenticated_client.post(employee_url, employee_payload, format=JSON_FORMAT)

        assert_error_response(response, status.HTTP_400_BAD_REQUEST)

    def test_returns_error_for_mismatched_job_title_and_department(
            self,
            authenticated_client,
            employee_url,
            employee_payload
    ):
        employee_payload[DEPARTMENT_FIELD] = MISMATCHED_DEPARTMENT
        response = authenticated_client.post(employee_url, employee_payload, format=JSON_FORMAT)

        assert_error_response(response, status.HTTP_400_BAD_REQUEST)
