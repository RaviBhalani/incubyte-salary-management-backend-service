from .env_helpers import get_env_var, get_int_env_var

POSTGRES_DB = get_env_var("POSTGRES_DB")
POSTGRES_USER = get_env_var("POSTGRES_USER")
POSTGRES_PASSWORD = get_env_var("POSTGRES_PASSWORD")
POSTGRES_HOST = get_env_var("POSTGRES_HOST")
POSTGRES_PORT = get_int_env_var("POSTGRES_PORT")

postgres_settings = {
    "ENGINE": "django.db.backends.postgresql_psycopg2",
    "NAME": POSTGRES_DB,
    "USER": POSTGRES_USER,
    "PASSWORD": POSTGRES_PASSWORD,
    "HOST": POSTGRES_HOST,
    "PORT": POSTGRES_PORT
}
