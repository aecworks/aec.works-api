import logging
from functools import lru_cache

from django.contrib.auth.models import Group, Permission

from api.images.services import create_image_asset, create_image_file_from_url

from .models import Profile, User

logger = logging.getLogger(__name__)


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


def create_group_and_permissions(groups_permissions: dict):
    # groups: dict[group_name]: [permission_names]
    # groups: { "editors": ["permission_names"]

    for group_name, permissions in groups_permissions.items():
        group, created = Group.objects.get_or_create(name=group_name)
        permissions = Permission.objects.filter(codename__in=permissions)
        view_permissions = Permission.objects.filter(codename__contains="view")
        group.permissions.set(permissions | view_permissions)
        logger.info(f"Created group: {group_name}: {permissions}")


def delete_group(group_name: str):
    Group.objects.filter(name=group_name).delete()
    logger.info(f"Deleted group: {group_name}")
