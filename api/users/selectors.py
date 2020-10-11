from api.users.models import Profile


def get_profiles():
    return Profile.objects.select_related("user").all()


def get_distinct_profiles():
    return Profile.objects.select_related("user").order_by("slug").distinct("slug")
