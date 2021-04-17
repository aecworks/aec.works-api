from django.core.management.base import BaseCommand

from api.users.models import User, UserProviderChoices


class Command(BaseCommand):
    help = "Fix Provider"

    def handle(self, *args, **options):
        for user in User.objects.all():
            old_provider = user.provider
            if user.provider in UserProviderChoices.__members__:
                print(f"VALID: {user}: {user.provider}")
            else:
                try:
                    should_be = UserProviderChoices(user.provider).name
                except ValueError:
                    should_be = UserProviderChoices.SIGN_UP.name
                user.provider = should_be
                user.save()
                print(f"FIXED: {user}: {old_provider} -> {should_be}")
