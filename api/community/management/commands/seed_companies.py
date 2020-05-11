import json

import requests
from io import BytesIO

from django.core.management.base import BaseCommand, CommandError
from django.core.files.images import ImageFile

from api.community.models import Company
from api.common.utils import to_slug


class Command(BaseCommand):
    help = "Closes the specified poll for voting"

    # def add_arguments(self, parser):
    #     parser.add_argument('poll_ids', nargs='+', type=int)

    def handle(self, *args, **options):

        url = "https://www.aecstartups.com/.netlify/functions/airtable"

        with open("aecstartups.json") as fp:
            data = json.load(fp)

        for record in data["records"]:
            record = record["fields"]
            crunchbase_id = get_crunchbase_id(record.get("crunchbase"))
            website = record.get("website")
            name = record.get("title")
            description = record.get("description")
            image_path = record.get("image")

            # TODO
            # tags = record["tags"]

            if not description or not name or not website:
                continue

            slug = to_slug(name)

            defaults = dict(
                name=name,
                crunchbase_id=crunchbase_id,
                description=description,
                website=website,
            )

            company, _ = Company.objects.update_or_create(slug=slug, defaults=defaults)

            # Image
            if image_path:
                logo = make_image(slug, image_path)
                if logo:
                    company.logo = logo

            company.save()
            msg = f"Created {company.slug}"
            self.stdout.write(self.style.SUCCESS(msg))


def get_crunchbase_id(url):
    return url.split("/")[-1] if url else None


"""
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
 'id': 'recW0FpRZMaQv5Ble'}
 """


def make_image(slug, path):
    if path.endswith("svg"):
        print(f"Cant add {slug}")
        return
    if path.startswith("logos"):
        path = f"https://www.aecstartups.com/{path}"

    resp = requests.get(path)
    if not resp.ok:
        print(f"failed: {slug}")
        return

    fp = BytesIO()
    fp.write(resp.content)

    ext = path.split(".")[-1]
    if ext not in ["jpg", "png", "jpge"]:
        ext = "png"
    filename = f"{slug}.{ext}"
    image = ImageFile(fp, name=filename)

    return image

