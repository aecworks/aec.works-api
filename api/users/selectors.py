from api.users.models import Profile


def get_profile(slug) -> Profile:
    return Profile.objects.select_related("user").get(slug=slug)


def get_profiles():
    return Profile.objects.select_related("user").all()
