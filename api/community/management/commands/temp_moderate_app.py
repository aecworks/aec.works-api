from django.core.management.base import BaseCommand

from api.community import choices, models, services
from api.users.models import Profile


class Command(BaseCommand):
    help = "Moderates all Companies"

    def add_arguments(self, parser):
        parser.add_argument("profile_slug", type=str)
        parser.add_argument("status", type=str)

    def handle(self, *args, **options):
        profile_slug = options["profile_slug"]
        arg_status = options["status"]

        try:
            choices.ModerationStatus[arg_status]
        except KeyError:
            raise Exception(f"invalid status: {arg_status}")

        profile = Profile.objects.get(slug=profile_slug)
        for co in models.Company.objects.all():
            services.moderate_company(
                profile=profile, company=co, status=arg_status,
            )
            print(f"APPROVED: {co}")
