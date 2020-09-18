from django.urls import path
from api.users import views


urlpatterns = [
    # /webhooks/
    path("twitter/", views.TwitterWebhookView.as_view()),
]
