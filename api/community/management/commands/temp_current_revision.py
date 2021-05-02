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
                    print(f"no revision available for: {co}")
