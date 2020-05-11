from django.urls import path
from api.users.views import ProfileListView


urlpatterns = [
    # /users/
    path("profiles/", ProfileListView.as_view())
]
