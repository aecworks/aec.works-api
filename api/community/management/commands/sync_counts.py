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

        for thread in models.Thread.objects.all():
            top_level_comments = models.Comment.objects.filter(
                thread_id=thread.id, level=0
            )
            thread_size = 0
            for top_level in top_level_comments:
                thread_size += top_level.get_descendants(include_self=True).count()
                thread.size = thread_size
                thread.save()

        for comment in models.Comment.objects.all():
            comment.reply_count = comment.get_children().count()
            comment.save()
