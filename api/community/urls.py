from django.urls import path
from api.community import views


urlpatterns = [
    # /community/
    path("comments/", views.CommentListView.as_view()),
    path("companies/", views.CompanyListView.as_view()),
    path("companies/<int:pk>/", views.CompanyDetailView.as_view()),
    path("posts/", views.PostListView.as_view()),
    path("posts/<int:pk>/", views.PostDetailView.as_view()),
    path("posts/<int:pk>/clap/", views.PostClapView.as_view()),
]
