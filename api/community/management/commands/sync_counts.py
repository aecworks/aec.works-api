from django.core.management.base import BaseCommand

from api.community import models


class Command(BaseCommand):
    help = "Sync Counts"

    def handle(self, *args, **options):

        for company in models.Company.objects.all():
            company.clap_count = company.clappers.count()
            company.save()

        for post in models.Post.objects.all():
            post.clap_count = post.clappers.count()
            post.save()

        for comment in models.Comment.objects.all():
            comment.clap_count = comment.clappers.count()
            comment.save()
