import pytest
from rest_framework import status

from apps.employee.tests.constants import (
    DATA_KEY,
    DEPARTMENT_FIELD,
    INVALID_DEPARTMENT,
    INVALID_JOB_TITLE,
    JOB_TITLE_FIELD,
    MISMATCHED_JOB_TITLE,
    NAME_FIELD,
    SALARY_FIELD,
    UPDATED_EMPLOYEE_NAME,
    UPDATED_EMPLOYEE_SALARY,
)
from tests.constants import JSON_FORMAT
from tests.helpers.assertions import assert_error_response

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

    def test_returns_error_for_invalid_job_title(self, authenticated_client, employee_detail_url, employee):
        response = authenticated_client.patch(
            employee_detail_url,
            {JOB_TITLE_FIELD: INVALID_JOB_TITLE},
            format=JSON_FORMAT,
        )

        assert_error_response(response, status.HTTP_400_BAD_REQUEST)

    def test_returns_error_for_invalid_department(self, authenticated_client, employee_detail_url, employee):
        response = authenticated_client.patch(
            employee_detail_url,
            {DEPARTMENT_FIELD: INVALID_DEPARTMENT},
            format=JSON_FORMAT,
        )

        assert_error_response(response, status.HTTP_400_BAD_REQUEST)

    def test_returns_error_for_mismatched_job_title_and_department(
            self,
            authenticated_client,
            employee_detail_url,
            employee,
    ):
        response = authenticated_client.patch(
            employee_detail_url,
            {JOB_TITLE_FIELD: MISMATCHED_JOB_TITLE},
            format=JSON_FORMAT,
        )

        assert_error_response(response, status.HTTP_400_BAD_REQUEST)
