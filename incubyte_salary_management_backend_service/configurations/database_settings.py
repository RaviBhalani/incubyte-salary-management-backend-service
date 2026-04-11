import dj_database_url

from apps.core.constants import LOCAL
from .common_settings import ENVIRONMENT
from .env_helpers import get_env_var, get_int_env_var


if ENVIRONMENT == LOCAL:
    postgres_settings = {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": get_env_var("POSTGRES_DB"),
        "USER": get_env_var("POSTGRES_USER"),
        "PASSWORD": get_env_var("POSTGRES_PASSWORD"),
        "HOST": get_env_var("POSTGRES_HOST"),
        "PORT": get_int_env_var("POSTGRES_PORT"),
    }
else:
    postgres_settings = dj_database_url.parse(get_env_var("POSTGRES_URL"))
