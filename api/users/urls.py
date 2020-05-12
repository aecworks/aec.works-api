from django.urls import path
from api.users import views


urlpatterns = [
    # /users/
    path("profiles/", views.ProfileListView.as_view()),
    path("profiles/<int:pk>/", views.ProfileDetailView.as_view()),
]
