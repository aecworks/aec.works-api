from django.urls import path
from api.images import views

urlpatterns = [
    # /images/
    # filename is required but not needed
    path("upload/<str:filename>", views.ImageUploadView.as_view()),
]
