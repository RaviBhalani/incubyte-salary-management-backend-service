from rest_framework import status

from apps.employee.tests.constants import (
    AVG_SALARY_FIELD,
    DATA_KEY,
    MAX_SALARY_FIELD,
    MIN_SALARY_FIELD,
    TEST_EMPLOYEE_SALARY,
    TOTAL_EMPLOYEES_FIELD,
)


def assert_salary_insights_filtered_to_employee(response):
    data = response.data[DATA_KEY]

    assert response.status_code == status.HTTP_200_OK
    assert data[TOTAL_EMPLOYEES_FIELD] == 1
    assert data[MIN_SALARY_FIELD] == TEST_EMPLOYEE_SALARY
    assert data[MAX_SALARY_FIELD] == TEST_EMPLOYEE_SALARY
    assert data[AVG_SALARY_FIELD] == TEST_EMPLOYEE_SALARY
