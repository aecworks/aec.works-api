import pytest
from api.community import factories as f
from api.users.factories import UserFactory
from rest_framework_simplejwt.tokens import AccessToken


@pytest.fixture
def jwt_auth_header(client, django_user_model):
    user = UserFactory()
    token = AccessToken.for_user(user)
    return dict(HTTP_AUTHORIZATION="JWT {}".format(token))


@pytest.mark.django_db
class TestViews:
    @pytest.mark.parametrize(
        "path,param_factory",
        [
            ["comments/?thread_id={0}", lambda: f.ThreadFactory().id],
            [
                "comments/?parent_id={0}",
                lambda: f.CommentFactory(thread=f.ThreadFactory()).id,
            ],
            ["companies/", lambda: f.CompanyFactory()],
            ["companies/{0}/", lambda: f.CompanyFactory().slug],
            ["posts/", lambda: f.PostFactory()],
            ["posts/{0}/", lambda: f.PostFactory().slug],
        ],
    )
    def test_get_views_annonymous(
        self, client, django_assert_max_num_queries, path, param_factory
    ):
        if param_factory:
            path = path.format(param_factory())
        url = f"/community/{path}"
        with django_assert_max_num_queries(5):
            resp = client.get(url)
            assert resp.status_code == 200

    def test_post_post(self, client, jwt_auth_header):
        url = "/community/posts/"
        payload = {
            "title": "Fake Title",
            "body": "Fake Body",
            "hashtags": [f.HashtagFactory().slug],
        }
        resp = client.post(url, payload)
        assert resp.status_code == 401

        resp = client.post(url, payload, **jwt_auth_header)
        assert resp.status_code == 201

    def test_post_patch(self, client, jwt_auth_header):
        post = f.PostFactory()
        token = AccessToken.for_user(post.profile.user)
        author_jwt_auth_header = dict(HTTP_AUTHORIZATION="JWT {}".format(token))

        url = f"/community/posts/{post.slug}/"
        payload = {
            "title": "Fake Title",
            "body": "Fake Body",
            "hashtags": [f.HashtagFactory().slug],
        }

        resp = client.patch(
            url, payload, content_type="application/json", **jwt_auth_header
        )
        # Token for random user cannot patch
        assert resp.status_code == 403
        # Token for author user can
        resp = client.patch(
            url, payload, content_type="application/json", **author_jwt_auth_header
        )
        assert resp.status_code == 200

    def test_company_patch(self, client, jwt_auth_header):
        company = f.CompanyFactory()
        token = AccessToken.for_user(company.profile.user)
        jwt_auth_header = dict(HTTP_AUTHORIZATION="JWT {}".format(token))

        url = f"/community/companies/{company.slug}/"
        payload = {
            "name": "Name",
            "description": "x",
            "employeeCount": "x",
            "hashtags": ["x"],
            "website": "https://www.x.com",
        }
        resp = client.patch(
            url, payload, content_type="application/json", **jwt_auth_header
        )
        assert resp.status_code == 200

    def test_post_clap(self, client, jwt_auth_header):
        post = f.PostFactory()
        url = f"/community/posts/{post.slug}/clap/"

        resp = client.post(url)
        assert resp.status_code == 401

        resp = client.post(url, **jwt_auth_header)
        assert resp.status_code == 200
