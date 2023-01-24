from django.core.management.base import BaseCommand

from api.community.models import Company, CompanyRevision
from api.images.models import ImageAsset
from api.images.services import create_image_file_from_url
from api.users.models import Profile


class Command(BaseCommand):
    help = "ImageAssetsFromUrl"

    def handle(self, *args, **options):
        """Temporary Script to migrate from url images to ImageAsset"""

        all_companies = [
            *list(Company.objects.all()),
            *list(CompanyRevision.objects.all()),
        ]
        for obj in all_companies:
            if obj.logo:
                img_file = create_image_file_from_url(obj.logo.file.url)
                img = ImageAsset.objects.create(file=img_file)
                obj.logo = img
                print(f"[{obj}] {img} for {obj.logo}")
                obj.save()

            if obj.cover:
                img_file = create_image_file_from_url(obj.cover.file.url)
                img = ImageAsset.objects.create(file=img_file)
                obj.cover = img
                print(f"[{obj}] {img} for {obj.cover}")
                obj.save()

        for obj in Profile.objects.all():
            if obj.avatar:
                img_file = create_image_file_from_url(obj.avatar_url)
                img = ImageAsset.objects.create(file=img_file)
                obj.avatar = img
                print(f"[{obj}] {img} for {obj.avatar_url}")
                obj.save()
