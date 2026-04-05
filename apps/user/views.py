from rest_framework_simplejwt.views import TokenObtainPairView

from apps.user.serializers import TokenObtainPairSerializer


class TokenObtainPairView(TokenObtainPairView):
    """
    Takes a set of user credentials and returns an access and refresh JSON web
    token pair to prove the authentication of those credentials.
    """

    serializer_class = TokenObtainPairSerializer
