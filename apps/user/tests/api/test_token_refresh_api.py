import pytest
from rest_framework import status

from apps.user.tests.constants import (
    ACCESS_TOKEN_KEY,
    INVALID_REFRESH_TOKEN,
    REFRESH_TOKEN_KEY,
)
from tests.constants import JSON_FORMAT
from tests.helpers import assert_error_response


pytestmark = pytest.mark.django_db


class TestTokenRefreshApi:

    def test_returns_access_token_for_valid_refresh_token(
        self,
        api_client,
        login_url,
        login_payload,
        token_refresh_url,
        login_user,
    ):
        login_response = api_client.post(
            login_url,
            login_payload,
            format=JSON_FORMAT,
        )

        refresh_response = api_client.post(
            token_refresh_url,
            {REFRESH_TOKEN_KEY: login_response.data[REFRESH_TOKEN_KEY]},
            format=JSON_FORMAT,
        )

        assert refresh_response.status_code == status.HTTP_200_OK
        assert ACCESS_TOKEN_KEY in refresh_response.data
        assert REFRESH_TOKEN_KEY not in refresh_response.data

    def test_returns_unauthorized_for_invalid_refresh_token(
        self,
        api_client,
        token_refresh_url,
    ):
        response = api_client.post(
            token_refresh_url,
            {REFRESH_TOKEN_KEY: INVALID_REFRESH_TOKEN},
            format=JSON_FORMAT,
        )

        assert_error_response(response, status.HTTP_401_UNAUTHORIZED)
