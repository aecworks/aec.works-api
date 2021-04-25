import debug_toolbar
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    # Sitemap
    path("", include("api.aecworks.sitemaps")),
    # Admin + Jet (Admin Skin)
    path("", admin.site.urls),
    path("jet/", include("jet.urls", "jet")),
    # DRF Browsable Api Auth
    path("api-auth/", include("rest_framework.urls")),
    # Djoser Auth - users, token
    path("auth/", include("djoser.urls")),
    # Apps
    path("community/", include("api.community.urls")),
    path("users/", include("api.users.urls")),
    path("images/", include("api.images.urls")),
    path("webhooks/", include("api.webhooks.urls")),
    # Debug Toolbar
    path("__debug__/", include(debug_toolbar.urls)),
]

if settings.MEDIA_ROOT:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
