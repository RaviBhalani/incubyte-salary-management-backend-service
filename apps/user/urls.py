from django.urls import include, path
from rest_framework_simplejwt.views import TokenRefreshView
from apps.user.views import TokenObtainPairView


urlpatterns = [
    path("login/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token-refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    
]
