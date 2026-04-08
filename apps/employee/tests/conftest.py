import pytest
from django.urls import reverse

from apps.employee.constants import EMPLOYEE_DETAIL_NAME, EMPLOYEE_LIST_NAME
from apps.employee.tests.constants import (
    TEST_EMPLOYEE_COUNTRY,
    TEST_EMPLOYEE_DEPARTMENT,
    TEST_EMPLOYEE_JOB_TITLE,
    TEST_EMPLOYEE_JOINING_DATE,
    TEST_EMPLOYEE_NAME,
    TEST_EMPLOYEE_SALARY,
)
from apps.employee.tests.factories import create_employee


@pytest.fixture
def employee_url():
    return reverse(EMPLOYEE_LIST_NAME)


@pytest.fixture
def employee_detail_url(employee):
    return reverse(EMPLOYEE_DETAIL_NAME, args=[employee.id])


@pytest.fixture
def employee_payload():
    return {
        "name": TEST_EMPLOYEE_NAME,
        "job_title": TEST_EMPLOYEE_JOB_TITLE,
        "department": TEST_EMPLOYEE_DEPARTMENT,
        "salary": TEST_EMPLOYEE_SALARY,
        "joining_date": TEST_EMPLOYEE_JOINING_DATE,
        "country": TEST_EMPLOYEE_COUNTRY,
    }


@pytest.fixture
def employee():
    return create_employee()


@pytest.fixture
def deleted_employee():
    return create_employee(is_active=False)


@pytest.fixture
def deleted_employee_detail_url(deleted_employee):
    return reverse(EMPLOYEE_DETAIL_NAME, args=[deleted_employee.id])
