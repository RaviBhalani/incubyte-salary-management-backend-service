from django.contrib import admin

from apps.employee.models import Employee


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ("employee_id", "name", "email", "job_title", "department", "salary", "country", "joining_date")
    search_fields = ("employee_id", "name", "email")
    list_filter = ("department", "country", "job_title")
    ordering = ("name",)
