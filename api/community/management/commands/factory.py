from django.core.management.base import BaseCommand

from api.community import factories as f


class Command(BaseCommand):
    help = "Factory Tests"

    def handle(self, *args, **options):
        c = f.CompanyFactory()
        print(c)
        print(c.current_revision)

        r = f.CompanyRevisionFactory(name="XXX", company__slug="xx")
        print(r)
        print(r.company)
        print(r.company.current_revision)
