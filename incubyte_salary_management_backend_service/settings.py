from os.path import join

from apps.employee.constants import EMPLOYEE_APP
from apps.user.constants import USER_APP
from .configurations.common_settings import BASE_DIR, APP_TITLE
from .configurations.database_settings import postgres_settings
from .configurations.env_helpers import get_env_var, get_bool_env_var, get_list_env_var, get_int_env_var
from .configurations.jwt_settings import SIMPLE_JWT
from .configurations.logger_settings import LOGGING
from .configurations.rest_framework_settings import REST_FRAMEWORK
from .configurations.spectacular_settings import SPECTACULAR_SETTINGS

""" 
Application Definition Start.
"""

ENVIRONMENT = get_env_var("ENVIRONMENT")
SECRET_KEY = get_env_var("SECRET_KEY")
DEBUG = get_bool_env_var("DEBUG")

ENABLE_TEAMS_NOTIFICATIONS = get_env_var("ENABLE_TEAMS_NOTIFICATIONS")
ENABLE_DJANGO_ADMIN = get_bool_env_var("ENABLE_DJANGO_ADMIN")
ENABLE_SWAGGER = get_bool_env_var("ENABLE_SWAGGER")

CORE_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

THIRD_PARTY_APPS = [
    "rest_framework",
    "corsheaders",
    "import_export",
    "drf_spectacular",
    "rest_framework_simplejwt.token_blacklist",
]

PROJECT_APPS = [
    USER_APP,
    EMPLOYEE_APP,
]

INSTALLED_APPS = CORE_APPS + PROJECT_APPS + THIRD_PARTY_APPS

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = True
ALLOWED_HOSTS = get_list_env_var("ALLOWED_HOSTS")
CSRF_TRUSTED_ORIGINS = get_list_env_var("CSRF_TRUSTED_ORIGINS")

ROOT_URLCONF = "incubyte_salary_management_backend_service.urls"
WSGI_APPLICATION = "incubyte_salary_management_backend_service.wsgi.application"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

"""
Application Definition End.
"""

""" 
Database Settings Start.
"""

DATABASES = {"default": postgres_settings}

""" 
Database Settings End.
"""

"""
Authentication & Authorization Settings Start.
"""

AUTH_USER_MODEL = "user.User"
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

PASSWORD_RESET_TIMEOUT = get_int_env_var("PASSWORD_RESET_TIMEOUT")

"""
Authentication & Authorization Settings End.
"""

"""
Internationalization Settings Start.
"""

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

"""
Internationalization Settings End.
"""


"""
Static Files Settings Start.
"""

STATIC_URL = "/static/"
STATIC_ROOT = join(BASE_DIR, "staticfiles")
STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
    },
}

"""
Static Files Settings End.
"""


"""
Teams Integration Settings Start
"""

TEAMS_WEBHOOK_URL = get_env_var("TEAMS_WEBHOOK_URL")

"""
Teams Integration Settings End
"""
