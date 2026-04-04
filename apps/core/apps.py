from django.apps import AppConfig

from apps.core.constants import CORE_APP


class CoreConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = CORE_APP
