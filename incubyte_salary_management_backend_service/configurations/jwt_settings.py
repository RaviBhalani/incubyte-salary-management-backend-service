from datetime import timedelta
from os.path import join

from apps.core.constants import LOCAL
from .common_settings import BASE_DIR, ENVIRONMENT
from .env_helpers import get_int_env_var, get_env_var


ACCESS_TOKEN_EXPIRY_DAYS = get_int_env_var("ACCESS_TOKEN_EXPIRY_DAYS")
ACCESS_TOKEN_EXPIRY_MINUTES = get_int_env_var("ACCESS_TOKEN_EXPIRY_MINUTES")
access_token_params = {
    'days': ACCESS_TOKEN_EXPIRY_DAYS,
    'minutes': ACCESS_TOKEN_EXPIRY_MINUTES
}

REFRESH_TOKEN_EXPIRY_DAYS = get_int_env_var("REFRESH_TOKEN_EXPIRY_DAYS")
REFRESH_TOKEN_EXPIRY_MINUTES = get_int_env_var("REFRESH_TOKEN_EXPIRY_MINUTES")
refresh_token_params = {
    'days': REFRESH_TOKEN_EXPIRY_DAYS,
    'minutes': REFRESH_TOKEN_EXPIRY_MINUTES
}

SLIDING_TOKEN_LIFETIME_MINUTES = get_int_env_var("SLIDING_TOKEN_LIFETIME_MINUTES")
SLIDING_TOKEN_REFRESH_LIFETIME_DAYS = get_int_env_var("SLIDING_TOKEN_REFRESH_LIFETIME_DAYS")

if ENVIRONMENT == LOCAL:
    RSA_PRIVATE_KEY_PATH = join(BASE_DIR, '.encryption_keys', get_env_var("RSA_PRIVATE_KEY"))
    RSA_PUBLIC_KEY_PATH = join(BASE_DIR, '.encryption_keys', get_env_var("RSA_PUBLIC_KEY"))
    RSA_SIGNING_KEY = open(RSA_PRIVATE_KEY_PATH).read()
    RSA_VERIFYING_KEY = open(RSA_PUBLIC_KEY_PATH).read()
else:
    RSA_SIGNING_KEY = get_env_var("RSA_PRIVATE_KEY").replace("\\n", "\n")
    RSA_VERIFYING_KEY = get_env_var("RSA_PUBLIC_KEY").replace("\\n", "\n")

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(**access_token_params),
    "REFRESH_TOKEN_LIFETIME": timedelta(**refresh_token_params),
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,
    "UPDATE_LAST_LOGIN": False,
    "ALGORITHM": "RS256",
    "AUDIENCE": None,
    "ISSUER": None,
    "AUTH_HEADER_TYPES": ("Bearer",),
    "AUTH_HEADER_NAME": "HTTP_AUTHORIZATION",
    "USER_ID_FIELD": "id",
    "USER_ID_CLAIM": "user_id",
    "AUTH_TOKEN_CLASSES": ("rest_framework_simplejwt.tokens.AccessToken",),
    "TOKEN_TYPE_CLAIM": "token_type",
    "JTI_CLAIM": "jti",
    "SLIDING_TOKEN_REFRESH_EXP_CLAIM": "refresh_exp",
    "SLIDING_TOKEN_LIFETIME": timedelta(minutes=SLIDING_TOKEN_LIFETIME_MINUTES),
    "SLIDING_TOKEN_REFRESH_LIFETIME": timedelta(days=SLIDING_TOKEN_REFRESH_LIFETIME_DAYS),
    "SIGNING_KEY": RSA_SIGNING_KEY,
    "VERIFYING_KEY": RSA_VERIFYING_KEY,
}
