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
            yield f.HashtagFactory()

    def handle(self, *args, **options):
        hashtag_generator = self.get_hashtag()
        profile = ProfileFactory()

        for _ in range(150):
            hashtag = next(hashtag_generator)
            thread = f.ThreadFactory()
            comments = [
                f.CommentFactory(profile=profile, thread=thread) for _ in range(25)
            ]
            comments[0].clappers.add(profile)
            comments[1].clappers.add(profile)

            post = f.PostFactory(profile=profile, thread=thread)
            post.hashtags.add(hashtag)
            post.clappers.add(profile)

        call_command("loaddata", "api/community/fixtures/companies.json")
