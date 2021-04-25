from django.core.management.base import BaseCommand

from api.users.groups import groups_permissions
from api.users.services import create_group_and_permissions, delete_group


class Command(BaseCommand):
    help = "Groups"

    def add_arguments(self, parser):
        parser.add_argument(
            "--delete", action="store_true", help="Delete groups instead of creating",
        )

    def handle(self, *args, **options):

        if options["delete"]:
            for name in groups_permissions.keys():
                delete_group(name)

        else:
            create_group_and_permissions(groups_permissions)
