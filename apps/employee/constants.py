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
EMPLOYEE_ID_PREFIX = "EMP"
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
CANNOT_REACTIVATE_DELETED_EMPLOYEE_MESSAGE = "Deleted employees cannot be reactivated."

"""
Validation message constants end.
"""
