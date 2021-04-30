# TODO rewrite with request factory for speed instead of client

import pytest

from api.community import factories as f
from api.images.factories import ImageAssetFactory
from api.users.factories import UserFactory


@pytest.mark.django_db
class TestViews:
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
        c_1 = f.CompanyFactory()
        c_2 = f.CompanyFactory()
        c_3 = f.CompanyFactory()
        c_1.current_revision.hashtags.set([a])
        c_2.current_revision.hashtags.set([a, b])
        c_3.current_revision.hashtags.set([a, b, c])

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
            "lastRevisionId": "",
        }
        resp = auth_client.post(url, payload, format="json")
        assert resp.status_code == 200
        created = resp.json()
        assert "A" in created["hashtags"]
        assert "B" in created["hashtags"]
        assert payload["website"] == created["website"]
        assert payload["description"] == created["description"]
        assert payload["twitter"] == created["twitter"]
        assert payload["crunchbaseId"] == created["crunchbaseId"]
        assert payload["logo"] == logo.id
        assert payload["cover"] == logo.id

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

    def test_company_clap(self, auth_client):
        company = f.CompanyFactory()
        url = f"/community/companies/{company.slug}/clap/"

        resp = auth_client.post(url)
        assert resp.status_code == 200
        assert resp.content == b"1"

    def test_company_list_sorting(self, client):
        for name, location in zip("cab", "yxz"):
            # f.CompanyFactory(name=name, location=location)
            f.CompanyRevisionFactory(name=name, location=location)

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
