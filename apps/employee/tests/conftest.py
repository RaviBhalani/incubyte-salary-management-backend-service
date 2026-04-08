import pytest
from django.urls import reverse

from apps.employee.constants import EMPLOYEE_DETAIL_NAME, EMPLOYEE_LIST_NAME
from apps.employee.tests.constants import (
    OTHER_EMPLOYEE_COUNTRY,
    OTHER_EMPLOYEE_DEPARTMENT,
    OTHER_EMPLOYEE_EMAIL,
    OTHER_EMPLOYEE_ID,
    OTHER_EMPLOYEE_JOB_TITLE,
    OTHER_EMPLOYEE_NAME,
    OTHER_EMPLOYEE_SALARY,
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
def other_employee():
    return create_employee(
        employee_id=OTHER_EMPLOYEE_ID,
        name=OTHER_EMPLOYEE_NAME,
        email=OTHER_EMPLOYEE_EMAIL,
        job_title=OTHER_EMPLOYEE_JOB_TITLE,
        department=OTHER_EMPLOYEE_DEPARTMENT,
        country=OTHER_EMPLOYEE_COUNTRY,
        salary=OTHER_EMPLOYEE_SALARY,
    )


@pytest.fixture
def deleted_employee():
    return create_employee(is_active=False)


@pytest.fixture
def deleted_employee_detail_url(deleted_employee):
    return reverse(EMPLOYEE_DETAIL_NAME, args=[deleted_employee.id])
