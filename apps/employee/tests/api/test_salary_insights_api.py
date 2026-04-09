import pytest
from rest_framework import status

from apps.employee.tests.constants import (
    AVG_SALARY_FIELD,
    DATA_KEY,
    MAX_SALARY_FIELD,
    MIN_SALARY_FIELD,
    OTHER_EMPLOYEE_SALARY,
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
