from unittest import mock
import pytest
from rest_framework.test import APIClient
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

    @mock.patch("api.users.views.services.get_jwt_for_user")
    @mock.patch("api.users.views.services.update_profile")
    @mock.patch("api.users.views.services.create_or_update_user")
    @mock.patch("api.users.views.GithubProvider.get_user_data_from_code")
    def test_oauth_login(
        self,
        m_get_user_data_from_code,
        m_create_or_update_user,
        m_update_profile,
        m_get_jwt_for_user,
        client,
    ):
        """ Test github/login/view """
        user = ProfileFactory().user
        m_get_user_data_from_code.return_value = user.email, {}, {}
        m_create_or_update_user.return_value = user
        m_get_jwt_for_user.return_value = {"access": "x", "refresh": "x"}

        resp = client.post("/users/login/github/?code=fakecode")

        assert resp.status_code == 200

        m_get_user_data_from_code.assert_called_once_with("fakecode")
        m_create_or_update_user.assert_called_once_with(
            email=user.email, defaults={"source": "github"}
        )
        m_update_profile.assert_called_once_with(user=user, defaults={})
        m_get_jwt_for_user.assert_called_once_with(user)

    def test_oauth_missing_code(self, client):
        resp = client.post("/users/login/github/")
        assert resp.status_code == 400

    def test_oauth_bad_provider(self, client):
        resp = client.post("/users/login/facebook/")
        assert resp.status_code == 400

    def test_profile_annon(self, client):
        resp = client.get("/users/profiles/me/")
        assert resp.status_code == 401

    def test_profile(self, django_user_model):
        user = django_user_model.objects.create(email="x@x.com", password="x")
        client = APIClient()
        client.force_authenticate(user=user)
        resp = client.get("/users/profiles/me/")
        assert resp.status_code == 200
