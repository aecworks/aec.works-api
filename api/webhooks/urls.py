from django.urls import path
from . import views


urlpatterns = [
    # /webhooks/
    path("twitter/", views.TwitterWebhookView.as_view()),
]
