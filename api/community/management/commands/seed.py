from django.core.management.base import BaseCommand
from api.users.factories import ProfileFactory
from api.community import models
from api.community import factories as f


class Command(BaseCommand):
    help = "Seed"

    def handle(self, *args, **options):
        profile = ProfileFactory()
        hashtag = f.Hashtag()

        for _ in range(10):
            thread = f.ThreadFactory()
            comment = f.CommentFaThreadFactory(profile=profile, thread=thread)
            comment_2 = f.CommentFaThreadFactory(profile=profile, thread=thread)
            [
                f.CommentFaThreadFactory(profile=profile, parent=comment)
                for _ in range(10)
            ]
            comment.clappers.add(profile)
            comment_2.clappers.add(profile)

            post = f.PostFaThreadFactory(profile=profile, thread=thread)
            post.hashtags.add(hashtag)
            post.clappers.add(profile)

        for company in models.Company.objects.all():
            thread = f.ThreadFactory()
            company.thread = thread
            company.save()

            comment = f.CommentFaThreadFactory(profile=profile, thread=thread)
            comment.clappers.add(profile)

            company.clappers.add(profile)
