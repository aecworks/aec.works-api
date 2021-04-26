from django.core.management.base import BaseCommand

from api.community import models


class Command(BaseCommand):
    help = "Sync Counts"

    def handle(self, *args, **options):

        for company in models.Company.objects.all():
            clap_count = company.clappers.count()
            models.Company.objects.filter(pk=company.id).update(clap_count=clap_count)

        for post in models.Post.objects.all():
            post.clap_count = post.clappers.count()
            post.save()

        for comment in models.Comment.objects.all():
            comment.clap_count = comment.clappers.count()
            comment.save()

        for thread in models.Thread.objects.all():
            thread.size = thread.comments.count()
            thread.save()
