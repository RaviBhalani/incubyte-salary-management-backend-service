import pytest
from django.urls import reverse
from rest_framework import status

from apps.employee.constants import EMPLOYEE_DETAIL_NAME
from apps.employee.tests.constants import (
    COUNTRY_FIELD,
    DATA_KEY,
    DEPARTMENT_FIELD,
    EMAIL_FIELD,
    EMPLOYEE_ID_FIELD,
    IS_ACTIVE_FIELD,
    JOB_TITLE_FIELD,
    JOINING_DATE_FIELD,
    NAME_FIELD,
    NONEXISTENT_EMPLOYEE_PK,
    SALARY_FIELD,
)
from tests.constants import JSON_FORMAT
from tests.helpers.assertions import assert_error_response

pytestmark = pytest.mark.django_db


class TestRetrieveEmployeeApi:

    def test_returns_employee_by_id(self, authenticated_client, employee_detail_url, employee):
        response = authenticated_client.get(employee_detail_url, format=JSON_FORMAT)

        data = response.data[DATA_KEY]
        assert response.status_code == status.HTTP_200_OK
        assert data[EMPLOYEE_ID_FIELD] == employee.employee_id
        assert data[EMAIL_FIELD] == employee.email
        assert data[NAME_FIELD] == employee.name
        assert data[JOB_TITLE_FIELD] == employee.job_title
        assert data[DEPARTMENT_FIELD] == employee.department
        assert data[SALARY_FIELD] == employee.salary
        assert data[JOINING_DATE_FIELD] == str(employee.joining_date)
        assert data[COUNTRY_FIELD] == employee.country
        assert data[IS_ACTIVE_FIELD] is True

    def test_returns_not_found_for_nonexistent_employee(self, authenticated_client):
        url = reverse(EMPLOYEE_DETAIL_NAME, args=[NONEXISTENT_EMPLOYEE_PK])
        response = authenticated_client.get(url, format=JSON_FORMAT)

        assert_error_response(response, status.HTTP_404_NOT_FOUND)

    def test_returns_not_found_for_deleted_employee(
            self,
            authenticated_client,
            deleted_employee_detail_url,
            deleted_employee
    ):

        response = authenticated_client.get(deleted_employee_detail_url, format=JSON_FORMAT)
        assert_error_response(response, status.HTTP_404_NOT_FOUND)
