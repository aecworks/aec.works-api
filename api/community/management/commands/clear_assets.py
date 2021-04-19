from django.core.management.base import BaseCommand

from api.community.models import Company, CompanyRevision
from api.users.models import Profile


class Command(BaseCommand):
    help = "ImageAssetsFromUrl"

    def handle(self, *args, **options):
        """ Temporary Script to migrate from url images to ImageAsset """

        all_companies = [
            *list(Company.objects.all()),
            *list(CompanyRevision.objects.all()),
        ]
        for obj in all_companies:
            if obj.logo:
                obj.logo = None
                obj.save()

            if obj.cover:
                obj.cover = None
                obj.save()

        for obj in Profile.objects.all():
            if obj.avatar:
                obj.avatar = None
                obj.save()
