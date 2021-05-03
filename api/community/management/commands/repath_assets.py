from django.core.management.base import BaseCommand

from api.images import services
from api.images.models import ImageAsset


class Command(BaseCommand):
    help = "Repath Image Assets"

    def add_arguments(self, parser):
        parser.add_argument("base_path", type=str)
        # for default `python manage.py repath_assets ""``

    def handle(self, *args, **options):
        base_path = options["base_path"] or "https://static.aec.works/"

        for asset in ImageAsset.objects.values("file", "id"):

            id = asset["id"]  # 'images/fbb090a62e2b40f282ff28a0438dcb09.jpeg'
            path = asset["file"]  # 'images/fbb090a62e2b40f282ff28a0438dcb09.jpeg'

            url = base_path + path
            new_img = services.create_image_file_from_url(url)
            new_img.name = f"images/{new_img.name}"
            ImageAsset.objects.filter(id=id).update(file=new_img)
            print(f"Saved: {url}")
