from django.contrib.auth import get_user_model

from tests.constants import TEST_USER_EMAIL, TEST_USER_PASSWORD


def create_user(*, email=TEST_USER_EMAIL, password=TEST_USER_PASSWORD):
    return get_user_model().objects.create_user(
        email=email,
        password=password,
    )
