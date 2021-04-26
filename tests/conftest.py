import pytest
from django.contrib.auth.models import Group
from django.core.management import call_command
from rest_framework.test import APIClient

from api.users.factories import UserFactory


@pytest.fixture(autouse=True)
def setup_groups(db):
    call_command("groups")


@pytest.fixture(autouse=True)
def use_in_memory_storage(settings):
    settings.DEFAULT_FILE_STORAGE = "inmemorystorage.InMemoryStorage"


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
