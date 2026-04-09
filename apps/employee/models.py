from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import IntegerField, Max
from django.db.models.functions import Cast, Substr

from apps.core.models import IsActive
from apps.employee.constants import (
    EMPLOYEE_COUNTRY_MAX_LENGTH,
    EMPLOYEE_DEPARTMENT_MAX_LENGTH,
    EMPLOYEE_ID_MAX_LENGTH,
    EMPLOYEE_ID_NUMERIC_START_INDEX,
    EMPLOYEE_JOB_TITLE_MAX_LENGTH,
    EMPLOYEE_NAME_MAX_LENGTH,
    EMPLOYEE_SALARY_MAX_VALUE,
    EMPLOYEE_SALARY_MIN_VALUE,
    Country,
    JobTitle,
)


class Employee(IsActive):
    employee_id = models.CharField(max_length=EMPLOYEE_ID_MAX_LENGTH, unique=True)
    name = models.CharField(max_length=EMPLOYEE_NAME_MAX_LENGTH)
    email = models.EmailField(unique=True)
    job_title = models.CharField(max_length=EMPLOYEE_JOB_TITLE_MAX_LENGTH, choices=JobTitle)
    department = models.CharField(max_length=EMPLOYEE_DEPARTMENT_MAX_LENGTH)
    salary = models.PositiveIntegerField(
        validators=[
            MinValueValidator(EMPLOYEE_SALARY_MIN_VALUE),
            MaxValueValidator(EMPLOYEE_SALARY_MAX_VALUE)
        ]
    )
    joining_date = models.DateField()
    country = models.CharField(max_length=EMPLOYEE_COUNTRY_MAX_LENGTH, choices=Country)

    class Meta:
        db_table = "employee"

    @classmethod
    def get_max_employee_number(cls):
        return cls.objects.aggregate(
            max_num=Max(Cast(Substr("employee_id", EMPLOYEE_ID_NUMERIC_START_INDEX), IntegerField()))
        )["max_num"] or 0

    def __str__(self):
        return self.name
