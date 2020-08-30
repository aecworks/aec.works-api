from .models import User, Profile


def create_or_update_user(*, email, defaults):
    user, _ = User.objects.update_or_create(email=email, defaults=defaults)
    return user


def update_profile(*, user, defaults):
    profile, _ = Profile.objects.update_or_create(user=user, defaults=defaults)
    return profile
