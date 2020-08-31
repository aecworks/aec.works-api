import pytest
from api.community import factories as f
from api.users.factories import UserFactory


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
        with django_assert_max_num_queries(8):
            resp = auth_client.get(url)
            assert resp.status_code == 200

    def test_get_companies_filter(self, auth_client):
        a = f.HashtagFactory(slug="a")
        b = f.HashtagFactory(slug="b")
        c_1 = f.CompanyFactory()
        c_2 = f.CompanyFactory()
        c_1.hashtags.set([a])
        c_2.hashtags.set([a, b])

        resp = auth_client.get("/community/companies/?hashtags=a")
        assert resp.json()["count"] == 2

        resp = auth_client.get("/community/companies/?hashtags=b")
        assert resp.json()["count"] == 1

    def test_post_post(self, api_client, auth_client):
        url = "/community/posts/"
        payload = {
            "title": "Fake Title",
            "body": "Fake Body",
            "hashtags": [f.HashtagFactory().slug],
        }
        resp = api_client.post(url, payload)
        assert resp.status_code == 403

        resp = auth_client.post(url, payload)
        assert resp.status_code == 201

    def test_post_patch(self, api_client):
        post = f.PostFactory()
        another_user = UserFactory(password="1")
        api_client.force_login(another_user)

        url = f"/community/posts/{post.slug}/"
        payload = {
            "title": "Fake Title",
            "body": "Fake Body",
            "hashtags": [f.HashtagFactory().slug],
        }

        resp = api_client.patch(url, payload, format="json")
        # Token for random user cannot patch
        assert resp.status_code == 403

        api_client.force_login(post.profile.user)
        # Token for author user can
        resp = api_client.patch(url, payload, format="json")
        assert resp.status_code == 200

    def test_company_revision(self, auth_client):
        company = f.CompanyFactory()

        url = f"/community/companies/{company.slug}/revisions/"
        payload = {
            "name": "Name",
            "description": "x",
            "hashtags": ["x"],
            "website": "https://www.x.com",
        }
        resp = auth_client.post(url, payload, format="json")
        assert resp.status_code == 200

    def test_post_clap(self, api_client, auth_client):
        post = f.PostFactory()
        url = f"/community/posts/{post.slug}/clap/"

        resp = api_client.post(url)
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
