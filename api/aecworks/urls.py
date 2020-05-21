from django.conf import settings
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("jet/", include("jet.urls", "jet")),
    path("admin/", admin.site.urls),
    # Allow Login in browseable API
    path("api-auth/", include("rest_framework.urls")),
    # Djoser Auth URL
    path("auth/", include("djoser.urls")),
    path("auth/", include("djoser.urls.jwt")),
    # path("auth/", include("djoser.urls.authtoken")),
    # Apps
    path("community/", include("api.community.urls")),
    path("users/", include("api.users.urls")),
]

if settings.DEBUG:
    import debug_toolbar  # noqa

    urlpatterns.append(path("__debug__/", include(debug_toolbar.urls)))

if settings.SERVE_STATIC:
    from django.conf.urls.static import static  # noqa
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns  # noqa

    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
