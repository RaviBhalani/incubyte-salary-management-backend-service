import jwt
from rest_framework_simplejwt.tokens import RefreshToken

from incubyte_salary_management_backend_service import settings


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    data = dict()
    data["refresh"] = str(refresh)
    access_token = str(refresh.access_token)

    decode_jwt = jwt.decode(
        access_token, settings.SIMPLE_JWT["VERIFYING_KEY"], algorithms=["RS256"]
    )

    decode_jwt["email"] = user.email
    decode_jwt["name"] = user.first_name
    decode_jwt["user_id"] = user.id

    # encode
    encoded = jwt.encode(
        decode_jwt, settings.SIMPLE_JWT["SIGNING_KEY"], algorithm="RS256"
    )

    data["access"] = encoded

    return data
