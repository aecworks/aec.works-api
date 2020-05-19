from django.contrib.auth import get_user_model
from api.users.models import Profile


User = get_user_model()


def get_profiles():
    return Profile.objects.select_related("user").all()


def get_or_create_user(*, email, defaults):
    user, _ = User.objects.update_or_create(email=email, defaults=defaults)
    return user
