from django.contrib.auth.models import Group, Permission
from django.core.management.base import BaseCommand

editor_permissions = [
    "add_companyrevision",
    "change_company",
    "apply_companyrevision",
    "add_company",
    "add_hashtag",
    "delete_company",
]
group_settings = {
    "editors": editor_permissions,
}


class Command(BaseCommand):
    help = "Groups"

    def add_arguments(self, parser):
        parser.add_argument(
            "--delete", action="store_true", help="Delete groups instead of creating",
        )

    def handle(self, *args, **options):

        if options["delete"]:
            print(f"deleting groups: {group_settings.keys()}")
            Group.objects.filter(name__in=group_settings.keys()).delete()

        else:
            for group_name, permissions in group_settings.items():
                group, created = Group.objects.get_or_create(name=group_name)
                permissions = Permission.objects.filter(codename__in=permissions)
                view_permissions = Permission.objects.filter(codename__contains="view")
                group.permissions.set(permissions | view_permissions)
                print(f"Created group: {group_name}: {permissions}")
