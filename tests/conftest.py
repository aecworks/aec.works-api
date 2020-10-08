import pytest
from django.contrib.auth.models import Group
from rest_framework.test import APIClient
from graphene_django.utils.testing import graphql_query

from api.users.factories import UserFactory


@pytest.fixture(scope="function")
def auth_client(db):
    user = UserFactory(password="1")
    group = Group.objects.get(name="editors")
    user.groups.add(group)

    client = APIClient()
    assert client.login(email=user.email, password="1")
    return client


@pytest.fixture
def gql_client(auth_client):
    def func(*args, **kwargs):
        return graphql_query(*args, **kwargs, client=auth_client)

    return func


@pytest.fixture(scope="function")
def api_client():
    return APIClient()
