# import io
# from django.core.files.images import ImageFile
from django.core.management.base import BaseCommand

from api.community.models import CompanyRevision

# from api.images.factories import png_bytes
from api.images.models import ImageAsset
from api.users.models import Profile

# from api.images import services


class Command(BaseCommand):
    help = "Purge Unused Assets"

    """ Deletes any Images Assets not referenced by Companies or Profiles """

    def handle(self, *args, **options):

        referenced_ids = set()
        for obj in CompanyRevision.objects.all():
            if obj.logo:
                referenced_ids.add(obj.logo.id)
            if obj.cover:
                referenced_ids.add(obj.cover.id)

        for obj in Profile.objects.all():
            if obj.avatar:
                referenced_ids.add(obj.avatar.id)

        print(f"Referenced: {len(referenced_ids)}")
        count = ImageAsset.objects.all().count()
        print(f"Total: {count}")

        orphans = ImageAsset.objects.exclude(id__in=referenced_ids).all()
        print(f"Orphans: {orphans.count()}")

        deleted, _ = orphans.delete()
        print(f"Deleted: {deleted}")
