from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.authtoken.models import Token


def get_jwt_for_user(user) -> dict:
    refresh = RefreshToken.for_user(user)
    return {"refresh": str(refresh), "access": str(refresh.access_token)}


def get_token_for_user(user) -> dict:
    token, _ = Token.objects.get_or_create(user=user)
    return token


def set_profile_data(*, user, profile_data):
    for key, value in profile_data.items():
        setattr(user.profile, key, value)
    user.profile.save()
