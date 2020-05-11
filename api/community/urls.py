from django.urls import path
from api.community import views


urlpatterns = [
    # /community/
    path("companies/", views.CompanyListView.as_view()),
    path("posts/", views.PostListView.as_view()),
    path("comments/", views.CommentListView.as_view()),
    path("comments/<int:pk>/", views.CommentDetailView.as_view()),
]
