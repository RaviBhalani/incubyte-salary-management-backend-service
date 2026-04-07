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
EMPLOYEE_DEPARTMENT_MAX_LENGTH = 150
EMPLOYEE_COUNTRY_MAX_LENGTH = 150


class JobTitle(TextChoices):
    SOFTWARE_ENGINEER = "SOFTWARE_ENGINEER", "Software Engineer"
    SENIOR_SOFTWARE_ENGINEER = "SENIOR_SOFTWARE_ENGINEER", "Senior Software Engineer"
    ENGINEERING_MANAGER = "ENGINEERING_MANAGER", "Engineering Manager"
    DATA_ANALYST = "DATA_ANALYST", "Data Analyst"
    PRODUCT_MANAGER = "PRODUCT_MANAGER", "Product Manager"
    HR_MANAGER = "HR_MANAGER", "HR Manager"


EMPLOYEE_JOB_TITLE_MAX_LENGTH = max(len(job.value) for job in JobTitle)

"""
Model constants end.
"""
