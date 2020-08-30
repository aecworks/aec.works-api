import pytest
from api.community import factories as f
from api.users.factories import UserFactory
from rest_framework_simplejwt.tokens import AccessToken


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
            ["hashtags/", lambda: f.HashtagFactory()],
            ["posts/", lambda: f.PostFactory()],
            ["posts/{0}/", lambda: f.PostFactory().slug],
        ],
    )
    def test_get_views_annonymous(
        self, auth_client, django_assert_max_num_queries, path, param_factory
    ):
        if param_factory:
            path = path.format(param_factory())
        url = f"/community/{path}"
        with django_assert_max_num_queries(6):
            resp = auth_client.get(url)
            assert resp.status_code == 200

    def test_post_post(self, client, auth_client):
        url = "/community/posts/"
        payload = {
            "title": "Fake Title",
            "body": "Fake Body",
            "hashtags": [f.HashtagFactory().slug],
        }
        resp = client.post(url, payload)
        assert resp.status_code == 403

        resp = auth_client.post(url, payload)
        assert resp.status_code == 201

    def test_post_patch(self, client, auth_client):
        post = f.PostFactory()

        url = f"/community/posts/{post.slug}/"
        payload = {
            "title": "Fake Title",
            "body": "Fake Body",
            "hashtags": [f.HashtagFactory().slug],
        }

        resp = client.patch(url, payload, content_type="application/json")
        # Token for random user cannot patch
        assert resp.status_code == 403
        # Token for author user can
        resp = auth_client.patch(url, payload, content_type="application/json",)
        assert resp.status_code == 200

    def test_company_patch(self, auth_client):
        company = f.CompanyFactory()

        url = f"/community/companies/{company.slug}/revisions/"
        payload = {
            "name": "Name",
            "description": "x",
            "hashtags": ["x"],
            "website": "https://www.x.com",
        }
        resp = auth_client.post(url, payload, content_type="application/json")
        assert resp.status_code == 200

    def test_post_clap(self, client, auth_client):
        post = f.PostFactory()
        url = f"/community/posts/{post.slug}/clap/"

        resp = client.post(url)
        assert resp.status_code == 403

        resp = auth_client.post(url)
        assert resp.status_code == 200
        assert resp.content == b"1"

    def test_company_clap(self, auth_client):
        company = f.CompanyFactory()
        url = f"/community/companies/{company.slug}/clap/"

        resp = auth_client.post(url)
        assert resp.status_code == 200
        assert resp.content == b"1"

    def test_post_comment_clap(self, client, auth_client):
        thread = f.ThreadFactory()
        comment = f.CommentFactory(thread=thread)
        url = f"/community/comments/{comment.id}/clap/"

        resp = client.post(url)
        assert resp.status_code == 403

        resp = auth_client.post(url)
        assert resp.status_code == 200
        assert resp.content == b"1"
