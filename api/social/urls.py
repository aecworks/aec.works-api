from django.urls import path
from . import views


urlpatterns = [
    # /social/
    path("twitter/timeline/<str:handle>", views.TweetTimelineView.as_view()),
]
