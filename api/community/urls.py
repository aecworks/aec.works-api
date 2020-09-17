from django.urls import path
from api.community import views


urlpatterns = [
    # /community/
    path("comments/", views.CommentListView.as_view()),
    path("comments/<int:id>/clap/", views.CommentClapView.as_view()),
    path("companies/", views.CompanyListView.as_view()),
    path("companies/<str:slug>/", views.CompanyDetailView.as_view()),
    path("companies/<str:slug>/clap/", views.CompanyClapView.as_view()),
    path("companies/<str:slug>/articles/", views.CompanyArticleListView.as_view()),
    path("revisions/<int:id>/<str:action>", views.CompanyRevisionDetailView.as_view()),
    path("companies/<str:slug>/revisions/", views.CompanyRevisionListView.as_view()),
    path("hashtags/", views.HashtagListView.as_view()),
    path("posts/", views.PostListView.as_view()),
    path("posts/<str:slug>/", views.PostDetailView.as_view()),
    path("posts/<str:slug>/clap/", views.PostClapView.as_view()),
]
