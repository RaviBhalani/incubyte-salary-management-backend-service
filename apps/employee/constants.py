from datetime import date
from pathlib import Path

"""
App name start.
"""

EMPLOYEE_APP = "apps.employee"

"""
App name end.
"""


"""
URL constants start.
"""

EMPLOYEE_URL = "employee"
EMPLOYEE_BASENAME = "employee"
EMPLOYEE_LIST_NAME = "employee-list"
EMPLOYEE_DETAIL_NAME = "employee-detail"
SALARY_INSIGHTS_ACTION_NAME = "employee-salary-insights"

"""
URL constants end.
"""


"""
Model constants start.
"""

from django.db.models import TextChoices

EMPLOYEE_ID_MAX_LENGTH = 13
EMPLOYEE_NAME_MAX_LENGTH = 300
EMPLOYEE_SALARY_MIN_VALUE = 10_000
EMPLOYEE_SALARY_MAX_VALUE = 1_000_000_000
EMPLOYEE_SALARY_STEP = 10_000
EMPLOYEE_ID_PREFIX = "EMP"
EMPLOYEE_ID_NUMERIC_START_INDEX = len(EMPLOYEE_ID_PREFIX) + 1
EMPLOYEE_EMAIL_PREFIX = "emp"
COMPANY_EMAIL_DOMAIN = "incubyte.com"


class JobTitle(TextChoices):
    SOFTWARE_ENGINEER = "SOFTWARE_ENGINEER", "Software Engineer"
    SENIOR_SOFTWARE_ENGINEER = "SENIOR_SOFTWARE_ENGINEER", "Senior Software Engineer"
    ENGINEERING_MANAGER = "ENGINEERING_MANAGER", "Engineering Manager"
    DATA_ANALYST = "DATA_ANALYST", "Data Analyst"
    PRODUCT_MANAGER = "PRODUCT_MANAGER", "Product Manager"
    HR_MANAGER = "HR_MANAGER", "HR Manager"


EMPLOYEE_JOB_TITLE_MAX_LENGTH = max(len(job.value) for job in JobTitle)


class Department(TextChoices):
    ENGINEERING = "ENGINEERING", "Engineering"
    MANAGEMENT = "MANAGEMENT", "Management"
    HR = "HR", "HR"


EMPLOYEE_DEPARTMENT_MAX_LENGTH = max(len(dept.value) for dept in Department)

class Country(TextChoices):
    UNITED_STATES = "UNITED_STATES", "United States"
    INDIA = "INDIA", "India"
    UNITED_KINGDOM = "UNITED_KINGDOM", "United Kingdom"
    GERMANY = "GERMANY", "Germany"
    CANADA = "CANADA", "Canada"
    AUSTRALIA = "AUSTRALIA", "Australia"


EMPLOYEE_COUNTRY_MAX_LENGTH = max(len(country.value) for country in Country)

JOB_TITLE_DEPARTMENT_MAP = {
    JobTitle.SOFTWARE_ENGINEER: Department.ENGINEERING,
    JobTitle.SENIOR_SOFTWARE_ENGINEER: Department.ENGINEERING,
    JobTitle.DATA_ANALYST: Department.ENGINEERING,
    JobTitle.ENGINEERING_MANAGER: Department.MANAGEMENT,
    JobTitle.PRODUCT_MANAGER: Department.MANAGEMENT,
    JobTitle.HR_MANAGER: Department.HR,
}

"""
Model constants end.
"""


"""
Validation message constants start.
"""

INVALID_JOB_TITLE_DEPARTMENT_MESSAGE = "Department does not match the job title."

"""
Validation message constants end.
"""


"""
Name file generation constants start.
"""

FAKER_LOCALE = "en_IN"
FIRST_NAMES_COUNT = 150
LAST_NAMES_COUNT = 100
FIRST_NAMES_FILENAME = "first_names.txt"
LAST_NAMES_FILENAME = "last_names.txt"
DATA_DIR_NAME = "data"
DATA_DIR = Path(__file__).resolve().parent / DATA_DIR_NAME
FIRST_NAMES_FILE = DATA_DIR / FIRST_NAMES_FILENAME
LAST_NAMES_FILE = DATA_DIR / LAST_NAMES_FILENAME
GENERATE_NAME_FILES_HELP = "Generate first_names.txt and last_names.txt with Indian names"
GENERATE_NAME_FILES_SUCCESS_MESSAGE = (
    "Written {first_count} first names to {first_file}\n"
    "Written {last_count} last names to {last_file}"
)

"""
Name file generation constants end.
"""


"""
Employee seed constants start.
"""

SEED_EMPLOYEES_COUNT = 10_000
BULK_CREATE_BATCH_SIZE = 500
SEED_JOINING_DATE_START = date(2015, 1, 1)
SEED_EMPLOYEES_HELP = "Seed 10,000 employee records from first_names.txt and last_names.txt"
SEED_EMPLOYEES_SUCCESS_MESSAGE = "Successfully seeded {count} employee records."

"""
Employee seed constants end.
"""
