from django.core.management.base import BaseCommand

from api.community.models import CompanyRevision
from api.images.models import ImageAsset
from api.users.models import Profile


class Command(BaseCommand):
    help = "ImageAssetsFromUrl"

    def handle(self, *args, **options):
        """ Temporary Script to migrate from url images to ImageAsset """

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
        print(orphans.count())
