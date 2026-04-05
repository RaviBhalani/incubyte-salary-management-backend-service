from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from apps.user.constants import (
    LOGIN_NAME,
    LOGIN_URL,
    TOKEN_REFRESH_NAME,
    TOKEN_REFRESH_URL,
)


urlpatterns = [
    path(LOGIN_URL, TokenObtainPairView.as_view(), name=LOGIN_NAME),
    path(
        TOKEN_REFRESH_URL,
        TokenRefreshView.as_view(),
        name=TOKEN_REFRESH_NAME,
    ),
]
