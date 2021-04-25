# TODO Replace with Request Factory Tests, much faster

from unittest import mock

import pytest
from rest_framework.test import APIClient

from api.users.auth import ProfileData, UserData
from api.users.choices import UserProviderChoices
from api.users.factories import ProfileFactory


@pytest.mark.django_db
class TestViews:
    @pytest.mark.parametrize(
        "path,param_factory",
        [["profiles/", None], ["profiles/{0}/", lambda: ProfileFactory().slug]],
    )
    def test_get_views_annonymous(self, client, path, param_factory):
        if param_factory:
            path = path.format(param_factory())
        url = f"/users/{path}"
        resp = client.get(url)
        assert resp.status_code == 200

    @mock.patch("api.users.views.services.update_profile")
    @mock.patch("api.users.views.services.create_or_update_user")
    @mock.patch("api.users.views.GithubProvider.get_user_data_from_code")
    def test_oauth_login(
        self,
        m_get_user_data_from_code,
        m_create_or_update_user,
        m_update_profile,
        client,
    ):
        """ Test github/login/view """
        user = ProfileFactory().user
        user_data = UserData(name="Fake Name", provider=UserProviderChoices.GITHUB.name)
        profile_data = ProfileData()
        m_get_user_data_from_code.return_value = (user.email, user_data, profile_data)
        m_create_or_update_user.return_value = user

        resp = client.post("/users/login/github/?code=fakecode&redirect_uri=fakeuri")

        assert resp.status_code == 200

        m_get_user_data_from_code.assert_called_once_with("fakecode", "fakeuri")
        m_create_or_update_user.assert_called_once_with(
            email=user.email, user_data=user_data
        )
        m_update_profile.assert_called_once_with(user=user, profile_data=profile_data)

    def test_oauth_missing_code(selfixi, client):
        resp = client.post("/users/login/github/")
        assert resp.status_code == 400

    def test_oauth_bad_provider(self, client):
        resp = client.post("/users/login/facebook/")
        assert resp.status_code == 400

    def test_profile_annon(self, client):
        resp = client.get("/users/profiles/me/")
        assert resp.status_code == 403

    def test_profile(self, django_user_model):
        user = django_user_model.objects.create(email="x@x.com", password="x")
        client = APIClient()
        client.force_authenticate(user=user)
        resp = client.get("/users/profiles/me/")
        assert resp.status_code == 200

    def test_login(self, django_user_model):
        name = "x"
        email = "x@x.com"
        password = "1"
        user = django_user_model(name=name, email=email)
        user.set_password(password)
        user.save()

        client = APIClient()
        resp = client.post("/users/login/", {"email": email, "password": password})
        assert resp.status_code == 200
        assert resp.json()["name"] == name
