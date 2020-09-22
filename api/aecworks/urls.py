from django.contrib import admin
from django.urls import path, include
import debug_toolbar
from django.views.generic import TemplateView
from rest_framework.schemas import get_schema_view

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
    path("images/", include("api.images.urls")),
    path("webhooks/", include("api.webhooks.urls")),
    # Debug Toolbar
    path("__debug__/", include(debug_toolbar.urls)),
    path(
        "redoc/",
        TemplateView.as_view(
            template_name="redoc.html", extra_context={"schema_url": "openapi-schema"}
        ),
        name="redoc",
    ),
    path(
        "openapi",
        get_schema_view(
            title="Your Project", description="API for all things …", version="1.0.0"
        ),
        name="openapi-schema",
    ),
]
