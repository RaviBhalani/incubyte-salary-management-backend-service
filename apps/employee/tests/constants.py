from apps.employee.constants import Department, EMPLOYEE_SALARY_MAX_VALUE, EMPLOYEE_SALARY_MIN_VALUE, JobTitle

"""
Employee test data constants start.
"""

TEST_EMPLOYEE_ID = "EMP0000000001"
TEST_EMPLOYEE_NAME = "John Doe"
TEST_EMPLOYEE_EMAIL = "john.doe@example.com"
TEST_EMPLOYEE_JOB_TITLE = JobTitle.SOFTWARE_ENGINEER
INVALID_JOB_TITLE = "Invalid Job Title"
TEST_EMPLOYEE_DEPARTMENT = Department.ENGINEERING
INVALID_DEPARTMENT = "Invalid Department"
MISMATCHED_DEPARTMENT = Department.MANAGEMENT
TEST_EMPLOYEE_SALARY = 50000
NEGATIVE_SALARY = -1
SALARY_BELOW_MINIMUM = EMPLOYEE_SALARY_MIN_VALUE - 1
SALARY_ABOVE_MAXIMUM = EMPLOYEE_SALARY_MAX_VALUE + 1
TEST_EMPLOYEE_JOINING_DATE = "2024-01-15"
TEST_EMPLOYEE_COUNTRY = "India"

UPDATED_EMPLOYEE_NAME = "Jane Doe"
UPDATED_EMPLOYEE_SALARY = 60000

"""
Employee test data constants end.
"""


"""
Employee response key constants start.
"""

EMPLOYEE_ID_FIELD = "employee_id"
NAME_FIELD = "name"
EMAIL_FIELD = "email"
JOB_TITLE_FIELD = "job_title"
DEPARTMENT_FIELD = "department"
SALARY_FIELD = "salary"
JOINING_DATE_FIELD = "joining_date"
COUNTRY_FIELD = "country"
DATA_KEY = "data"
RESULTS_KEY = "results"

"""
Employee response key constants end.
"""
