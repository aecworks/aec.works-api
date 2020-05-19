"""aecguide URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
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
