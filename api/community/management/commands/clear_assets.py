from django.core.management.base import BaseCommand

from api.community.models import Company, CompanyRevision
from api.users.models import Profile


class Command(BaseCommand):
    help = "ImageAssetsFromUrl"

    def handle(self, *args, **options):
        """ Temporary Script to migrate from url images to ImageAsset """

        for obj in CompanyRevision.objects.all():
            obj.logo = None
            obj.cover = None
            obj.save()

        for obj in Profile.objects.all():
            obj.avatar = None
            obj.save()
