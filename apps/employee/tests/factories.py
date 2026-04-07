from apps.employee.models import Employee
from apps.employee.tests.constants import (
    TEST_EMPLOYEE_COUNTRY,
    TEST_EMPLOYEE_DEPARTMENT,
    TEST_EMPLOYEE_EMAIL,
    TEST_EMPLOYEE_ID,
    TEST_EMPLOYEE_JOB_TITLE,
    TEST_EMPLOYEE_JOINING_DATE,
    TEST_EMPLOYEE_NAME,
    TEST_EMPLOYEE_SALARY,
)


def create_employee(
    *,
    employee_id=TEST_EMPLOYEE_ID,
    name=TEST_EMPLOYEE_NAME,
    email=TEST_EMPLOYEE_EMAIL,
    job_title=TEST_EMPLOYEE_JOB_TITLE,
    department=TEST_EMPLOYEE_DEPARTMENT,
    salary=TEST_EMPLOYEE_SALARY,
    joining_date=TEST_EMPLOYEE_JOINING_DATE,
    country=TEST_EMPLOYEE_COUNTRY,
):
    return Employee.objects.create(
        employee_id=employee_id,
        name=name,
        email=email,
        job_title=job_title,
        department=department,
        salary=salary,
        joining_date=joining_date,
        country=country,
    )
