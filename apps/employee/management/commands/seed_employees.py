import random
from datetime import date, timedelta

from django.core.management.base import BaseCommand

from apps.employee.constants import (
    BULK_CREATE_BATCH_SIZE,
    COMPANY_EMAIL_DOMAIN,
    Country,
    EMPLOYEE_EMAIL_PREFIX,
    EMPLOYEE_ID_PREFIX,
    EMPLOYEE_SALARY_MAX_VALUE,
    EMPLOYEE_SALARY_MIN_VALUE,
    EMPLOYEE_SALARY_STEP,
    FIRST_NAMES_FILE,
    JOB_TITLE_DEPARTMENT_MAP,
    JobTitle,
    LAST_NAMES_FILE,
    SEED_EMPLOYEES_COUNT,
    SEED_EMPLOYEES_HELP,
    SEED_EMPLOYEES_SUCCESS_MESSAGE,
    SEED_JOINING_DATE_START,
)
from apps.employee.models import Employee


class Command(BaseCommand):
    help = SEED_EMPLOYEES_HELP

    def handle(self, *args, **options):
        first_names = FIRST_NAMES_FILE.read_text().splitlines()
        last_names = LAST_NAMES_FILE.read_text().splitlines()

        start_num = Employee.get_max_employee_number() + 1

        job_titles = list(JobTitle)
        countries = list(Country)
        date_range = (date.today() - SEED_JOINING_DATE_START).days

        employees = [
            Employee(
                employee_id=f"{EMPLOYEE_ID_PREFIX}{i}",
                name=f"{random.choice(first_names)} {random.choice(last_names)}",
                email=f"{EMPLOYEE_EMAIL_PREFIX}_{i}@{COMPANY_EMAIL_DOMAIN}",
                job_title=(job_title := random.choice(job_titles)),
                department=JOB_TITLE_DEPARTMENT_MAP[job_title],
                salary=random.randrange(EMPLOYEE_SALARY_MIN_VALUE, EMPLOYEE_SALARY_MAX_VALUE + 1, EMPLOYEE_SALARY_STEP),
                joining_date=SEED_JOINING_DATE_START + timedelta(days=random.randint(0, date_range)),
                country=random.choice(countries),
            )
            for i in range(start_num, start_num + SEED_EMPLOYEES_COUNT)
        ]

        Employee.objects.bulk_create(employees, batch_size=BULK_CREATE_BATCH_SIZE)

        self.stdout.write(self.style.SUCCESS(
            SEED_EMPLOYEES_SUCCESS_MESSAGE.format(count=SEED_EMPLOYEES_COUNT)
        ))
