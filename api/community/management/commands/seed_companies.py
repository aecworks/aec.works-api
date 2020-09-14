from django.utils.text import slugify
import requests
from io import BytesIO

"""
WIP - this will be used to pull and sync aecstartups.com data
"""

from django.core.management.base import BaseCommand
from django.core.files.images import ImageFile

from api.community.models import Company
from api.community import services
from api.images.models import Image
from api.users.models import Profile


class Command(BaseCommand):
    help = "Closes the specified poll for voting"

    def add_arguments(self, parser):

        parser.add_argument(
            "--update",
            action="store_true",
            default=False,
            help="Update if slug clashes with one already defined",
        )

    def handle(self, *args, **options):

        should_update = options["update"]

        url = "https://www.aecstartups.com/.netlify/functions/airtable"
        resp = requests.get(url)
        data = resp.json()

        profile = Profile.objects.first()

        for record in data["records"]:
            record = record["fields"]
            crunchbase_id = get_crunchbase_id(record.get("crunchbase"))
            website = record.get("website")
            name = record.get("title")
            description = record.get("description")
            image_path = record.get("image")
            location = record.get("location", "Somewhere")

            tags = record.get("tags", [])

            if not description or not name or not website:
                msg = f"{name}-{website} Skiped: No Name or Desc. or Website"
                self.stdout.write(self.style.ERROR(msg))
                continue

            slug = slugify(name)

            defaults = dict(
                name=name,
                crunchbase_id=crunchbase_id,
                description=description,
                website=website,
                location=location,
                created_by=profile,
            )

            exists = Company.objects.filter(slug=slug).exists()

            if not exists:
                print(f"Creating: {slug}")
                company = Company.objects.create(slug=slug, **defaults)
            else:
                if not should_update:
                    print(f"Already exist: {slug}")
                    continue
                print(f"Updating exist: {slug}")
                company, _ = Company.objects.update_or_create(
                    slug=slug, defaults=defaults
                )

            # Image
            if image_path:
                logo = make_image(slug, image_path)
                if logo:
                    img = Image.objects.create(image=logo)
                    company.logo_url = img.image.url
                    company.cover_url = ""

            company.save()

            # Hashtags
            hashtags = services.get_or_create_hashtags(tags)
            company.hashtags.set(hashtags)

            msg = f"Created {company.slug}"
            self.stdout.write(self.style.SUCCESS(msg))


def get_crunchbase_id(url):
    return url.split("/")[-1] if url else None


"""
 'id': 'recW0FpRZMaQv5Ble'}
 'fields': {'created_on': '2019-06-05T19:17:34.000Z',
            'crunchbase': 'https://www.crunchbase.com/Company/3d-repo',
            'description': 'Cloud-Based BIM',
            'funding': 'Seed',
            'image': 'logos/3drepo.png',
            'industries': ['architecture', 'construction'],
            'location': 'London, UK',
            'proposed_by': '@gtalarico',
            'review': 'approved',
            'tags': ['web app', 'issue tracking', 'change management'],
            'title': '3D Repo',
            'website': 'https://3drepo.com'},
 """


def make_image(slug, path):
    if path.endswith("svg"):
        print(f"{slug}: Cant add svg image")
        return
    if path.startswith("logos"):
        path = f"https://www.aecstartups.com/{path}"

    resp = requests.get(path)
    if not resp.ok:
        print(f"{slug}: try getting relative logo but failed")
        return

    fp = BytesIO()
    fp.write(resp.content)

    ext = path.split(".")[-1]
    if ext not in ["jpg", "png", "jpge"]:
        ext = "png"
    filename = f"{slug}.{ext}"
    image = ImageFile(fp, name=filename)

    return image
