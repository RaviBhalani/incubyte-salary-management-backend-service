from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from apps.user.forms import UserDetailsChangeForm, UserDetailsCreationForm
from apps.user.models import User


class UserDetailsAdmin(UserAdmin):
    """
    Custom admin for User model
    """

    form = UserDetailsChangeForm
    add_form = UserDetailsCreationForm

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "email",
                    "first_name",
                    "password",

                )
            },
        ),
        (
            "Permissions",
            {"fields": ("email_verified", "is_active", "is_staff", "is_superuser")},
        ),
        ("Groups", {"fields": ("groups",)}),
    )

    add_fieldsets = (
        (None, {"classes": ("wide",), "fields": ("email", "password1", "password2")}),
    )

    list_display = (
        "id",
        "email",
        "first_name",
        "email_verified",
        "is_active",
        "created_ts",
        "modified_ts",
    )
    list_filter = ("is_superuser",

                   )
    search_fields = ("email", "first_name")
    ordering = ("email",)

admin.site.register(User, UserDetailsAdmin)
