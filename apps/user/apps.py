from django.apps import AppConfig

from apps.core.constants import USER_APP


class UserConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = USER_APP
