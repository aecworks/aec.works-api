from django.core.management.base import BaseCommand
from api.users.factories import ProfileFactory
from api.community import factories


class Command(BaseCommand):
    help = "Seed"

    def handle(self, *args, **options):
        profile = ProfileFactory()
        hashtag = factories.Hashtag()

        for _ in range(10):
            thread = factories.Thread()
            comment = factories.Comment(profile=profile, thread=thread)
            comment_2 = factories.Comment(profile=profile, thread=thread)
            [factories.Comment(profile=profile, parent=comment) for _ in range(10)]
            comment.clappers.add(profile)
            comment_2.clappers.add(profile)

            post = factories.Post(profile=profile, thread=thread)
            post.hashtags.add(hashtag)
            post.clappers.add(profile)
            factories.Company()
