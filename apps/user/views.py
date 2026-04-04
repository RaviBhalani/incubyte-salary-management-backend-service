from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.views import TokenObtainPairView
from apps.user.serializers import (
    TokenObtainPairSerializer,
    UserListSerializer,
    UserSerializer,
)
from apps.core.views import BaseViewset, BaseListModelMixin
from rest_framework.viewsets import ReadOnlyModelViewSet
from apps.user.models import (
    User,
)


class TokenObtainPairView(TokenObtainPairView):
    """
    Takes a set of user credentials and returns an access and refresh JSON web
    token pair to prove the authentication of those credentials.
    """

    serializer_class = TokenObtainPairSerializer


class UserListViewSet(ReadOnlyModelViewSet):
    """
    List users
    """

    serializer_class = UserListSerializer
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,
                          
                          )
    queryset = User.objects.all()


class UserViewsets(BaseViewset):
    """
    Viewset for User crud operations
    """
    serializer_class = UserSerializer
    ordering = ("-modified_ts")
    queryset = User.objects.all()

