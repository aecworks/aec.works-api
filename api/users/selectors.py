from api.users.models import Profile


def get_profiles():
    return Profile.objects.select_related("user").all()
