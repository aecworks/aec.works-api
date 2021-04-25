from functools import lru_cache

from api.images.services import create_image_asset, create_image_file_from_url

from .models import Profile, User


def create_or_update_user(*, email, user_data):
    defaults = user_data._asdict()
    user, _ = User.objects.update_or_create(email=email, defaults=defaults)
    return user


def update_profile(*, user, profile_data):
    defaults = profile_data._asdict()
    avatar_url = defaults.pop("avatar_url", None)
    if avatar_url:
        img_file = create_image_file_from_url(avatar_url)
        img_asset = create_image_asset(img_file=img_file, profile=user.profile)
        defaults["avatar"] = img_asset
    profile, _ = Profile.objects.update_or_create(user=user, defaults=defaults)
    return profile


@lru_cache()
def default_avatar(email):
    initials = email[:2].upper()
    return f"https://avatars.dicebear.com/api/initials/{initials}.svg"
