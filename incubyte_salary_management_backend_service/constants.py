from apps.core.url_builder import build_url


"""
URLs start.
"""

V1_API_PREFIX = "api/v1/"

ADMIN_URL = "admin/"

SCHEMA_URL = "schema/"
V1_SCHEMA_URL = build_url(V1_API_PREFIX, SCHEMA_URL)
SCHEMA_V1_NAME = "schema-v1"

DOCS_URL = "docs/"
V1_DOCS_URL = build_url(V1_API_PREFIX, DOCS_URL)
SWAGGER_UI_V1_NAME = "swagger-ui-v1"

"""
URLs end.
"""
