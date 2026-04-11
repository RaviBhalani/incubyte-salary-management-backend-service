import pytest
from django.urls import reverse

from apps.user.constants import LOGIN_NAME, LOGOUT_NAME, TOKEN_REFRESH_NAME
from apps.user.tests.constants import (
    LOGIN_TEST_USER_EMAIL,
    LOGIN_TEST_USER_PASSWORD,
)
from tests.factories.user import create_user


@pytest.fixture
def login_url():
    return reverse(LOGIN_NAME)


@pytest.fixture
def token_refresh_url():
    return reverse(TOKEN_REFRESH_NAME)


@pytest.fixture
def logout_url():
    return reverse(LOGOUT_NAME)


@pytest.fixture
def login_payload():
    return {
        "email": LOGIN_TEST_USER_EMAIL,
        "password": LOGIN_TEST_USER_PASSWORD,
    }


@pytest.fixture
def login_user():
    return create_user(
        email=LOGIN_TEST_USER_EMAIL,
        password=LOGIN_TEST_USER_PASSWORD,
    )
