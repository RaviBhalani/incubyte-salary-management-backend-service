import pytest
from rest_framework.test import APIClient

from tests.factories.user import create_user


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def authenticated_client(api_client):
    user = create_user()
    api_client.force_authenticate(user=user)
    return api_client
