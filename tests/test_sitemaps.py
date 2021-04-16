import pytest


@pytest.mark.django_db
class TestSitemapViews:
    @pytest.mark.parametrize(
        "path",
        [
            "/sitemaps/sitemap.xml",
            "/sitemaps/sitemap-home.xml",
            "/sitemaps/sitemap-companies.xml",
        ],
    )
    def test_sitemaps(self, client, path):
        resp = client.get(path)
        assert resp.status_code == 200
