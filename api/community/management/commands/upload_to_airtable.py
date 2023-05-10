import os

from django.core.management.base import BaseCommand
from pyairtable import Table
from pyairtable.utils import attachment

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
            # *list(CompanyRevision.objects.all()),
        ]
        table = Table(os.environ["AIRTABLE_API_KEY"], "appNtnZ99fkL1cByn", "Dump")
        records = []
        for company in all_companies:

            record = dict(
                Name=company.current_revision.name,
                Description=company.current_revision.description,
                Location=company.current_revision.location,
                Website=company.current_revision.website,
                Twitter=company.current_revision.twitter,
                Crunchbase=company.current_revision.crunchbase_id,
                Hashtags=",".join(
                    [h.slug for h in company.current_revision.hashtags.all()]
                ),
            )
            # "__sized__/images/5b1e142f5e214b2a9591eeda0df3c469-crop-c0-5__0-5-800x400.png"
            # https://raw.githubusercontent.com/gtalarico/aec-works-archive/master/images/__sized__/images/3975150367e6432497211a44ff5451e1-crop-c0-5__0-5-800x400.png

            base_url = "https://raw.githubusercontent.com/gtalarico/aec-works-archive/master/images/"
            try:
                cover_url = (
                    base_url + company.current_revision.cover.file.crop["800x400"].name
                )
                record["Cover"] = [
                    attachment(
                        cover_url, f"cover-400x800-{company.current_revision.name}"
                    )
                ]
            except Exception:
                pass
            try:
                logo_url = (
                    base_url + company.current_revision.logo.file.crop["80x80"].name
                )
                record["Logo"] = [
                    attachment(logo_url, f"logo-80x80-{company.current_revision.name}")
                ]
            except Exception:
                pass
            records.append(record)

        table.batch_create(records)
