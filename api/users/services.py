from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.authtoken.models import Token
from .models import User, Profile


def get_jwt_for_user(user) -> dict:
    refresh = RefreshToken.for_user(user)
    return {"refresh": str(refresh), "access": str(refresh.access_token)}


def get_token_for_user(user) -> dict:
    token, _ = Token.objects.get_or_create(user=user)
    return token


# def set_profile_data(*, user, profile_data):
#     for key, value in profile_data.items():
#         setattr(user.profile, key, value)
#     user.profile.save()


def create_or_update_user(*, email, defaults):
    user, _ = User.objects.update_or_create(email=email, defaults=defaults)
    return user


def update_profile(*, user, defaults):
    profile, _ = Profile.objects.update_or_create(user=user, defaults=defaults)
    return profile
