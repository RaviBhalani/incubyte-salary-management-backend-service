from django.urls import path
from rest_framework_simplejwt.views import TokenBlacklistView, TokenObtainPairView, TokenRefreshView

from apps.user.constants import (
    LOGIN_NAME,
    LOGIN_URL,
    LOGOUT_NAME,
    LOGOUT_URL,
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
    path(
        LOGOUT_URL,
        TokenBlacklistView.as_view(),
        name=LOGOUT_NAME,
    ),
]
