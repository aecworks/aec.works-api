from django.urls import path
from api.community import views


urlpatterns = [
    # /community/
    path("comments/", views.CommentListView.as_view()),
    path("companies/", views.CompanyListView.as_view()),
    path("companies/<str:slug>/", views.CompanyDetailView.as_view()),
    path("posts/", views.PostListView.as_view()),
    path("posts/<str:slug>/", views.PostDetailView.as_view()),
    path("posts/<str:slug>/clap/", views.PostClapView.as_view()),
]
