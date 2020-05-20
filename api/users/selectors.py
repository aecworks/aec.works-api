from django.contrib.auth import get_user_model
from api.users.models import Profile


User = get_user_model()


def get_profiles():
    return Profile.objects.select_related("user").all()
