from django.contrib.auth import get_user_model

User = get_user_model()


def get_or_create_user(*, email, defaults):
    user, _ = User.objects.update_or_create(email=email, defaults=defaults)
    return user
