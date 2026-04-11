import random
from datetime import date, timedelta

from django.db import migrations
from faker import Faker


FAKER_LOCALE = "en_IN"
FIRST_NAMES_COUNT = 150
LAST_NAMES_COUNT = 100
SEED_EMPLOYEES_COUNT = 10_000
BULK_CREATE_BATCH_SIZE = 500
EMPLOYEE_ID_PREFIX = "EMP"
EMPLOYEE_EMAIL_PREFIX = "emp"
COMPANY_EMAIL_DOMAIN = "incubyte.com"
EMPLOYEE_SALARY_MIN_VALUE = 10_000
EMPLOYEE_SALARY_MAX_VALUE = 1_000_000
EMPLOYEE_SALARY_STEP = 10_000
SEED_JOINING_DATE_START = date(2015, 1, 1)


def seed_employees(apps, schema_editor):
    Employee = apps.get_model("employee", "Employee")

    fake = Faker(FAKER_LOCALE)

    first_names = list({fake.first_name() for _ in range(FIRST_NAMES_COUNT * 5)})[:FIRST_NAMES_COUNT]
    last_names = list({fake.last_name() for _ in range(LAST_NAMES_COUNT * 5)})[:LAST_NAMES_COUNT]

    job_title_department_map = {
        "SOFTWARE_ENGINEER": "ENGINEERING",
        "SENIOR_SOFTWARE_ENGINEER": "ENGINEERING",
        "DATA_ANALYST": "ENGINEERING",
        "ENGINEERING_MANAGER": "MANAGEMENT",
        "PRODUCT_MANAGER": "MANAGEMENT",
        "HR_MANAGER": "HR",
    }

    job_titles = list(job_title_department_map.keys())
    countries = ["UNITED_STATES", "INDIA", "UNITED_KINGDOM", "GERMANY", "CANADA", "AUSTRALIA"]
    date_range = (date.today() - SEED_JOINING_DATE_START).days

    start_num = 1

    employees = [
        Employee(
            employee_id=f"{EMPLOYEE_ID_PREFIX}{i}",
            name=f"{random.choice(first_names)} {random.choice(last_names)}",
            email=f"{EMPLOYEE_EMAIL_PREFIX}_{i}@{COMPANY_EMAIL_DOMAIN}",
            job_title=(job_title := random.choice(job_titles)),
            department=job_title_department_map[job_title],
            salary=random.randrange(
                EMPLOYEE_SALARY_MIN_VALUE,
                EMPLOYEE_SALARY_MAX_VALUE + 1,
                EMPLOYEE_SALARY_STEP,
            ),
            joining_date=SEED_JOINING_DATE_START + timedelta(days=random.randint(0, date_range)),
            country=random.choice(countries),
        )
        for i in range(start_num, start_num + SEED_EMPLOYEES_COUNT)
    ]

    Employee.objects.bulk_create(employees, batch_size=BULK_CREATE_BATCH_SIZE)


class Migration(migrations.Migration):

    dependencies = [
        ("employee", "0010_alter_employee_salary"),
    ]

    operations = [
        migrations.RunPython(seed_employees, reverse_code=migrations.RunPython.noop),
    ]
