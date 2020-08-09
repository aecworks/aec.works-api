from django.core.management.base import BaseCommand
from django.core.management import call_command
from api.users.factories import ProfileFactory
from api.community import models
from api.community import factories as f


class Command(BaseCommand):
    help = "Seed"

    @staticmethod
    def get_hashtag():
        while True:
            for hashtag in models.Hashtag.objects.all():
                yield hashtag
            yield f.Hashtag()

    def handle(self, *args, **options):
        hashtag_generator = self.get_hashtag()
        profile = ProfileFactory()

        for _ in range(10):
            hashtag = next(hashtag_generator)
            thread = f.ThreadFactory()
            comment = f.CommentFactory(profile=profile, thread=thread)
            comment_2 = f.CommentFactory(profile=profile, thread=thread)
            [f.CommentFactory(profile=profile, parent=comment) for _ in range(10)]
            comment.clappers.add(profile)
            comment_2.clappers.add(profile)

            post = f.PostFactory(profile=profile, thread=thread)
            post.hashtags.add(hashtag)
            post.clappers.add(profile)

        call_command("loaddata", "api/community/fixtures/companies.json")
        # for company in models.Company.objects.all():
        #     thread = f.ThreadFactory()
        #     company.thread = thread
        #     company.save()
        #     comment = f.CommentFaThreadFactory(profile=profile, thread=thread)
        #     comment.clappers.add(profile)
        #     company.clappers.add(profile)
