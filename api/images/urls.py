from django.urls import path
from api.images import views

urlpatterns = [
    # /images/
    path("upload/<str:filename>", views.ImageUploadView.as_view()),
]
