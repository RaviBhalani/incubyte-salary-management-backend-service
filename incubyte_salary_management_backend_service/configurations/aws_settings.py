from boto3 import client
from botocore.config import Config

from apps.core.url_builder import build_url
from .env_helpers import get_env_var


AWS_ACCESS_KEY_ID = get_env_var("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = get_env_var("AWS_SECRET_ACCESS_KEY")
AWS_STORAGE_BUCKET_NAME = get_env_var("AWS_STORAGE_BUCKET_NAME")
AWS_S3_OBJECT_PARAMETERS = {"CacheControl": "max-age=86400"}
AWS_S3_PRE_SIGNED_POST_TIMEOUT = 600
AWS_S3_SIGNATURE_VERSION = "s3v4"
AWS_REGION_NAME = get_env_var("AWS_REGION_NAME")
AWS_LOCATION = "static"
AWS_S3_USE_SSL = True
AWS_DEFAULT_ACL = None
AWS_S3_CUSTOM_DOMAIN = f"{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com"
AWS_S3_FILE_KEY_PREFIX: str = "media/project_files/"
AWS_S3_BASE_URL = f"https://{AWS_S3_CUSTOM_DOMAIN}"

STATIC_URL = build_url(AWS_S3_BASE_URL, AWS_LOCATION)
STORAGES = {
    "default": {
        "BACKEND": "storages.backends.s3.S3Storage",
    },
    "staticfiles": {"BACKEND": "storages.backends.s3.S3Storage"},
}

params = {
    "service_name": "s3",
    "region_name": AWS_REGION_NAME,
    "config": Config(signature_version=AWS_S3_SIGNATURE_VERSION),
}
if AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY:
    params.update({
        "aws_access_key_id": AWS_ACCESS_KEY_ID,
        "aws_secret_access_key": AWS_SECRET_ACCESS_KEY,
    })

s3_client = client(**params)
