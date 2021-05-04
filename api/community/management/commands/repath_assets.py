from django.core.management.base import BaseCommand

from api.images import services
from api.images.models import ImageAsset


class Command(BaseCommand):
    help = "Repath Image Assets"
    """
    This script is used to allow dump from prod/staging to be re-pathed
    Let's say a prod dump includes Image asset where file: images/abc.png prod-s3

    This script will:
    * detect abc.png does not exist in current storage
    * fetch s3://prod-s3/images/abc.png
    * create a placeholder asset, and assign file to the local object
    * remove placeholder

    """

    def add_arguments(self, parser):
        parser.add_argument("base_path", type=str)
        # for default `python manage.py repath_assets ""``

    def handle(self, *args, **options):
        base_path = options["base_path"] or "https://static.aec.works/"

        for asset in ImageAsset.objects.values("file", "id"):

            id = asset["id"]  # 'images/fbb090a62e2b40f282ff28a0438dcb09.jpeg'
            path = asset["file"]  # 'images/fbb090a62e2b40f282ff28a0438dcb09.jpeg'

            try:
                i = ImageAsset.objects.get(id=id)
                i.file.crop["80x80"].url
                print(f"Looks good: {asset}")
                continue
            except Exception:
                print(f"Bad path: {asset}")

            url = base_path + path
            new_img = services.create_image_file_from_url(url)

            # Create placeholder asset
            ph = ImageAsset.objects.create(created_by=None, file=new_img)

            # Reassign
            ImageAsset.objects.filter(id=id).update(file=ph.file)

            qs = ImageAsset.objects.filter(id=ph.id)
            # Raw delete to prevent deleting actual file
            qs._raw_delete(qs.db)

            print(f"Replaced: {url}")
