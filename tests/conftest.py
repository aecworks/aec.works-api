import pytest

from api.users.factories import UserFactory
from rest_framework.test import APIClient


@pytest.fixture(scope="function")
def auth_client(db):
    user = UserFactory(password="1")
    client = APIClient()
    assert client.login(email=user.email, password="1")
    return client


@pytest.fixture(scope="function")
def api_client():
    return APIClient()
