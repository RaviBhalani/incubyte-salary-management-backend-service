from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

from .constants import (
    ADMIN_URL,
    V1_API_PREFIX,
    V1_SCHEMA_URL,
    V1_DOCS_URL,
    SCHEMA_V1_NAME,
    SWAGGER_UI_V1_NAME,
)

urlpatterns_v1 = [
    path(
        V1_API_PREFIX,
        include("apps.user.urls"),
    ),
]

urlpatterns = []

if settings.ENABLE_DJANGO_ADMIN:
    urlpatterns += [path(ADMIN_URL, admin.site.urls)]

if settings.ENABLE_SWAGGER:
    urlpatterns += [
        path(
            V1_SCHEMA_URL,
            SpectacularAPIView.as_view(api_version="v1", patterns=urlpatterns_v1),
            name=SCHEMA_V1_NAME,
        ),
        path(
            V1_DOCS_URL,
            SpectacularSwaggerView.as_view(url_name=SCHEMA_V1_NAME),
            name=SWAGGER_UI_V1_NAME,
        ),
    ]

urlpatterns += urlpatterns_v1