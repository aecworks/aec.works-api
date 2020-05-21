from django.conf import settings
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
]

if settings.DEBUG:
    urlpatterns.append(path("__debug__/", include(debug_toolbar.urls)))

# if settings.SERVE_STATIC:
#     from django.conf.urls.static import static  # noqa
#     from django.contrib.staticfiles.urls import staticfiles_urlpatterns  # noqa

#     urlpatterns += staticfiles_urlpatterns()
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
