from apps.core.url_builder import build_url

ADMIN_URL = "admin/"

V1_API_PREFIX = "api/v1/"

V1_SCHEMA_URL = build_url(V1_API_PREFIX, "schema/")
V1_DOCS_URL = build_url(V1_API_PREFIX, "docs/")

SCHEMA_V1_NAME = "schema-v1"
SWAGGER_UI_V1_NAME = "swagger-ui-v1"