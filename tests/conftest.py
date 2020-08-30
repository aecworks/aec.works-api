import pytest

from api.users.factories import UserFactory


@pytest.fixture
def auth_client(client, django_user_model):
    user = UserFactory(password="1")
    assert client.login(email=user.email, password="1")
    return client
