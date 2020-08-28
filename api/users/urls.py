from django.urls import path
from api.users import views


urlpatterns = [
    # /users/
    path("profiles/", views.ProfileListView.as_view()),
    path("profiles/me/", views.ProfileMeView.as_view()),
    path("profiles/<str:slug>/", views.ProfileDetailView.as_view()),
    path("login/<str:provider_name>/", views.OauthLoginView.as_view()),
]
