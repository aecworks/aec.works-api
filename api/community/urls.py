from django.urls import path

from api.community import views

urlpatterns = [
    # /community/
    path("comments/<int:thread_id>/", views.CommentListView.as_view()),
    path("comments/<int:id>/clap", views.CommentClapView.as_view()),
    path("companies/", views.CompanyListView.as_view()),
    path("companies/claps/<str:profile>/", views.CompanyProfileClapsListView.as_view()),
    path("companies/<str:slug>/", views.CompanyDetailView.as_view()),
    path("companies/<str:slug>/clap", views.CompanyClapView.as_view()),
    path("companies/<str:slug>/moderate", views.CompanyModerateView.as_view()),
    path("companies/<str:slug>/articles/", views.CompanyArticleListView.as_view()),
    path("revisions/<int:id>/<str:action>", views.CompanyRevisionDetailView.as_view()),
    path("companies/<str:slug>/revisions/", views.CompanyRevisionListView.as_view()),
    path("hashtags/", views.HashtagListView.as_view()),
]
