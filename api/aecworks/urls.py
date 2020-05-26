from django.contrib import admin
from django.urls import path, include
import debug_toolbar

urlpatterns = [
    # Admin + Jet (Admin Skin)
    path("admin/", admin.site.urls),
    path("jet/", include("jet.urls", "jet")),
    # DRF Browsable Api Auth
    path("api-auth/", include("rest_framework.urls")),
    # Djoser Auth - users, token and jwt urls
    path("auth/", include("djoser.urls")),
    path("auth/", include("djoser.urls.jwt")),
    # Apps
    path("community/", include("api.community.urls")),
    path("users/", include("api.users.urls")),
    # Debug Toolbar
    path("__debug__/", include(debug_toolbar.urls)),
]
