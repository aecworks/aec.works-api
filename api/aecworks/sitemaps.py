from django.contrib.sitemaps import Sitemap
from django.contrib.sitemaps import views as sitemap_views
from django.urls import path
from django.views.decorators.cache import cache_page


class IndexSitemap(Sitemap):
    changefreq = "weekly"
    priority = 1

    def items(self):
        return ["/", "/about", "/companies"]

    def location(self, obj):
        return obj


class CompanySitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.9

    def items(self):
        from api.community.selectors import get_companies  # noqa

        return [f"/companies/{c.slug}/" for c in get_companies()]

    def location(self, obj):
        return obj


sitemaps = dict(home=IndexSitemap, companies=CompanySitemap,)


urlpatterns = [
    path(
        "sitemaps/sitemap.xml",
        cache_page(60)(sitemap_views.index),
        {"sitemaps": sitemaps, "sitemap_url_name": "sitemaps"},
    ),
    path(
        "sitemaps/sitemap-<section>.xml",
        cache_page(60)(sitemap_views.sitemap),
        {"sitemaps": sitemaps},
        name="sitemaps",
    ),
]
