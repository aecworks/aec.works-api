# TODO rewrite with request factory for speed instead of client

import pytest

from api.community import choices
from api.community import factories as f
from api.community import services
from api.images.factories import ImageAssetFactory
from api.users.factories import ProfileFactory


@pytest.mark.django_db
class TestCommunityViews:
    @pytest.mark.parametrize(
        "path,param_factory",
        [
            ["comments/{0}/", lambda: f.ThreadFactory().id],
            ["companies/", lambda: [f.CompanyFactory() for _ in range(3)]],
            ["companies/{0}/", lambda: f.CompanyFactory().slug],
            ["hashtags/", lambda: [f.HashtagFactory() for _ in range(3)]],
        ],
    )
    def test_get_views_annonymous(
        self, auth_client, django_assert_max_num_queries, path, param_factory
    ):
        if param_factory:
            path = path.format(param_factory())
        url = f"/community/{path}"
        with django_assert_max_num_queries(10):
            resp = auth_client.get(url)
            assert resp.status_code == 200

    def test_get_companies_filter(self, auth_client):
        a = f.HashtagFactory(slug="a")
        b = f.HashtagFactory(slug="b")
        c = f.HashtagFactory(slug="c")
        status = choices.ModerationStatus.APPROVED.name
        f.CompanyFactory(status=status, current_revision__hashtags=[a])
        f.CompanyFactory(status=status, current_revision__hashtags=[a, b])
        f.CompanyFactory(status=status, current_revision__hashtags=[a, b, c])

        resp = auth_client.get("/community/companies/?hashtags=a")
        assert resp.json()["count"] == 3

        resp = auth_client.get("/community/companies/?hashtags=a,b")
        assert resp.json()["count"] == 2

        resp = auth_client.get("/community/companies/?hashtags=a,b,c")
        assert resp.json()["count"] == 1

    def test_company_create(self, auth_client):
        logo = ImageAssetFactory()
        url = "/community/companies/"
        payload = {
            "name": "Test 1",
            "description": "asdasd",
            "location": "São Paulo, Brazil",
            "website": "https://aec.works",
            "twitter": "xxx",
            "crunchbaseId": "zzz",
            "logo": logo.id,
            "cover": logo.id,
            "hashtags": ["A", "B"],
        }
        resp = auth_client.post(url, payload, format="json")
        assert resp.status_code == 200

        company = resp.json()
        rev = company["currentRevision"]

        assert "A" in rev["hashtags"]
        assert "B" in rev["hashtags"]
        assert payload["website"] == rev["website"]
        assert payload["description"] == rev["description"]
        assert payload["twitter"] == rev["twitter"]
        assert payload["crunchbaseId"] == rev["crunchbaseId"]
        assert payload["logo"] == logo.id
        assert payload["cover"] == logo.id

        assert rev["logoUrl"]
        assert rev["coverUrl"]

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

    def test_company_revision_apply(self, auth_client):
        company = f.CompanyFactory()
        rev = f.CompanyRevisionFactory(company=company)
        assert company.current_revision != rev
        url = f"/community/revisions/{rev.id}/apply"

        resp = auth_client.post(url)
        company.refresh_from_db()

        assert resp.status_code == 200
        assert company.current_revision == rev

    def test_company_moderate(self, auth_client):
        company = f.CompanyFactory(status="UNMODERATED")
        url = f"/community/companies/{company.slug}/moderation/"

        payload = {"status": "REJECTED"}
        resp_post = auth_client.post(url, payload, format="json")
        company.refresh_from_db()

        assert resp_post.status_code == 200
        assert company.status == "REJECTED"

        resp_get = auth_client.get(url)
        assert resp_get.status_code == 200
        assert resp_get.json()[0]["status"] == "REJECTED"

    def test_company_revision_moderate(self, auth_client):
        company = f.CompanyFactory(current_revision__status="UNMODERATED")
        rev = company.current_revision
        assert rev.status == "UNMODERATED"
        url = f"/community/revisions/{rev.id}/moderation/"

        TARGET_STATUS = "REJECTED"

        payload = {"status": TARGET_STATUS}
        resp_post = auth_client.post(url, payload, format="json")

        rev.refresh_from_db()

        assert resp_post.status_code == 200
        assert rev.status == TARGET_STATUS

        resp_get = auth_client.get(url)
        assert resp_get.status_code == 200
        assert resp_get.json()[0]["status"] == TARGET_STATUS

    def test_company_revision_history(self, auth_client):
        company = f.CompanyFactory(current_revision__status="UNMODERATED")
        rev = f.CompanyRevisionFactory(company=company)
        f.CompanyRevisionHistoryFactory(revision=rev)

        url = f"/community/companies/{company.slug}/revision-history/"

        resp = auth_client.get(url)

        assert resp.status_code == 200
        assert resp.json()[0]["revisionId"] == rev.id

    def test_company_clap(self, auth_client):
        company = f.CompanyFactory()
        url = f"/community/companies/{company.slug}/clap"

        resp = auth_client.post(url)
        assert resp.status_code == 200
        assert resp.content == b"1"

    def test_comment_clap(self, auth_client):
        comment = f.CommentFactory()
        url = f"/community/comments/{comment.id}/clap"

        resp = auth_client.post(url)
        assert resp.status_code == 200
        assert resp.content == b"1"

    def test_company_list_sorting(self, client):
        for name, location in zip("cab", "yxz"):
            f.CompanyFactory(
                status=choices.ModerationStatus.APPROVED.name,
                current_revision__name=name,
                current_revision__location=location,
            )

        url = "/community/companies/?sort=name"
        resp = client.get(url)
        assert resp.status_code == 200
        assert (
            resp.json()["results"][0]["currentRevision"]["name"] == "a"
        )  # lowest company name

        url = "/community/companies/?sort=name&reverse=1"
        assert client.get(url).json()["results"][0]["currentRevision"]["name"] == "c"

        url = "/community/companies/?sort=location"
        assert (
            client.get(url).json()["results"][0]["currentRevision"]["location"] == "x"
        )

        url = "/community/companies/?sort=location&reverse=1"
        assert (
            client.get(url).json()["results"][0]["currentRevision"]["location"] == "z"
        )

    def test_profile_company_claps(self, auth_client):
        profile = ProfileFactory()
        co = f.CompanyFactory(current_revision__name="X")
        services.company_clap(company=co, profile=profile)
        resp = auth_client.get(f"/community/companies/claps/{profile.slug}/")
        assert resp.status_code == 200
