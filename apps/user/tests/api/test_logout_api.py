import pytest
from rest_framework import status

from apps.user.tests.constants import (
    INVALID_REFRESH_TOKEN,
    REFRESH_TOKEN_KEY,
)
from tests.constants import JSON_FORMAT
from tests.helpers.assertions import assert_error_response

pytestmark = pytest.mark.django_db


class TestLogoutApi:

    def test_blacklists_refresh_token_and_returns_ok_for_valid_token(
        self,
        api_client,
        login_url,
        login_payload,
        logout_url,
        login_user,
    ):
        login_response = api_client.post(login_url, login_payload, format=JSON_FORMAT)
        refresh_token = login_response.data[REFRESH_TOKEN_KEY]

        response = api_client.post(
            logout_url,
            {REFRESH_TOKEN_KEY: refresh_token},
            format=JSON_FORMAT,
        )

        assert response.status_code == status.HTTP_200_OK

    def test_blacklisted_token_cannot_be_used_again(
        self,
        api_client,
        login_url,
        login_payload,
        logout_url,
        token_refresh_url,
        login_user,
    ):
        login_response = api_client.post(login_url, login_payload, format=JSON_FORMAT)
        refresh_token = login_response.data[REFRESH_TOKEN_KEY]

        api_client.post(
            logout_url,
            {REFRESH_TOKEN_KEY: refresh_token},
            format=JSON_FORMAT,
        )

        response = api_client.post(
            token_refresh_url,
            {REFRESH_TOKEN_KEY: refresh_token},
            format=JSON_FORMAT,
        )

        assert_error_response(response, status.HTTP_401_UNAUTHORIZED)

    def test_returns_unauthorized_for_invalid_refresh_token(
        self,
        api_client,
        logout_url,
    ):
        response = api_client.post(
            logout_url,
            {REFRESH_TOKEN_KEY: INVALID_REFRESH_TOKEN},
            format=JSON_FORMAT,
        )

        assert_error_response(response, status.HTTP_401_UNAUTHORIZED)

    def test_returns_bad_request_when_refresh_token_is_missing(
        self,
        api_client,
        logout_url,
    ):
        response = api_client.post(logout_url, {}, format=JSON_FORMAT)

        assert_error_response(response, status.HTTP_400_BAD_REQUEST)
