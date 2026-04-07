from django.db import models

from apps.employee.constants import (
    EMPLOYEE_COUNTRY_MAX_LENGTH,
    EMPLOYEE_DEPARTMENT_MAX_LENGTH,
    EMPLOYEE_ID_MAX_LENGTH,
    EMPLOYEE_JOB_TITLE_MAX_LENGTH,
    EMPLOYEE_NAME_MAX_LENGTH,
    JobTitle,
)


class Employee(models.Model):
    employee_id = models.CharField(max_length=EMPLOYEE_ID_MAX_LENGTH, unique=True)
    name = models.CharField(max_length=EMPLOYEE_NAME_MAX_LENGTH)
    email = models.EmailField(unique=True)
    job_title = models.CharField(max_length=EMPLOYEE_JOB_TITLE_MAX_LENGTH, choices=JobTitle)
    department = models.CharField(max_length=EMPLOYEE_DEPARTMENT_MAX_LENGTH)
    salary = models.IntegerField()
    joining_date = models.DateField()
    country = models.CharField(max_length=EMPLOYEE_COUNTRY_MAX_LENGTH)

    class Meta:
        db_table = "employee"

    def __str__(self):
        return self.name
