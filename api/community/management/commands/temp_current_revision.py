from django.core.management.base import BaseCommand

from api.community import models


class Command(BaseCommand):
    help = "Revision"

    def handle(self, *args, **options):

        for co in models.Company.objects.all():

            if not co.current_revision:
                print(f"Company '{co}' does not have a current revision")

                last_rev = models.CompanyRevision.objects.filter(company=co).last()

                if last_rev:
                    co.current_revision = last_rev
                    co.save()
                    print("set revision to last")
                else:
                    print(f"no revision available for: {co} - creating...")

                    rev = models.CompanyRevision.objects.create(
                        company=co,
                        created_by=co.created_by,
                        name=co.name,
                        description=co.description,
                        location=co.location,
                        website=co.website,
                        twitter=co.twitter,
                        crunchbase_id=co.crunchbase_id,
                        logo=co.logo,
                        cover=co.cover,
                    )
                    rev.hashtags.set(co.hashtags.all())
                    co.current_revision = rev
                    co.save()
