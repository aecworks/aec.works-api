import pytest
from django.contrib.auth.models import Group
from api.users.factories import UserFactory
from rest_framework.test import APIClient


@pytest.fixture(scope="function")
def auth_client(db):
    user = UserFactory(password="1")
    group = Group.objects.get(name="editors")
    user.groups.add(group)

    client = APIClient()
    assert client.login(email=user.email, password="1")
    return client


@pytest.fixture(scope="function")
def api_client():
    return APIClient()
