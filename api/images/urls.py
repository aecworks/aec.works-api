from django.urls import path

from api.images import views

urlpatterns = [
    # /images/...
    path("upload/", views.ImageAssetUploadView.as_view()),
    path("upload/<str:filename>", views.ImageAssetUploadView.as_view()),
]
