import pytest
from rest_framework import status

from apps.user.tests.constants import (
    ACCESS_TOKEN_KEY,
    DEFAULT_TEST_USER_EMAIL,
    INVALID_LOGIN_TEST_USER_PASSWORD,
    PASSWORD_FIELD,
    REFRESH_TOKEN_KEY,
)
from tests.constants import JSON_FORMAT
from tests.factories.user import create_user
from tests.helpers import assert_error_response

pytestmark = pytest.mark.django_db


class TestLoginApi:

    def test_returns_access_and_refresh_tokens_for_valid_credentials(
        self,
        api_client,
        login_url,
        login_payload,
        login_user,
    ):
        response = api_client.post(
            login_url,
            login_payload,
            format=JSON_FORMAT,
        )

        assert response.status_code == status.HTTP_200_OK
        assert ACCESS_TOKEN_KEY in response.data
        assert REFRESH_TOKEN_KEY in response.data

    def test_returns_unauthorized_for_invalid_credentials(
        self,
        api_client,
        login_url,
    ):
        create_user()
        response = api_client.post(
            login_url,
            {
                "email": DEFAULT_TEST_USER_EMAIL,
                "password": INVALID_LOGIN_TEST_USER_PASSWORD,
            },
            format=JSON_FORMAT,
        )

        assert_error_response(response, status.HTTP_401_UNAUTHORIZED)

    def test_returns_bad_request_when_password_is_missing(
        self,
        api_client,
        login_url,
    ):
        response = api_client.post(
            login_url,
            {
                "email": DEFAULT_TEST_USER_EMAIL,
            },
            format=JSON_FORMAT,
        )

        assert_error_response(response, status.HTTP_400_BAD_REQUEST)
        assert any(PASSWORD_FIELD in error for error in response.data["error_list"])
