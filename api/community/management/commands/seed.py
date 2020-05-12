import json

import requests
from io import BytesIO

from django.core.management.base import BaseCommand, CommandError

from api.users.factories import UserFactory, ProfileFactory
from api.community import factories


class Command(BaseCommand):
    help = "Seed"

    # def add_arguments(self, parser):
    #     parser.add_argument('poll_ids', nargs='+', type=int)

    def handle(self, *args, **options):
        profile = ProfileFactory()
        hashtag = factories.Hashtag()

        thread = factories.CommentThread()
        comment = factories.Comment(profile=profile, thread=thread)
        comment_2 = factories.Comment(profile=profile, thread=thread)
        [factories.Comment(profile=profile, parent=comment) for _ in range(30)]

        comment.clappers.add(profile)
        comment_2.clappers.add(profile)

        for _ in range(10):
            post = factories.Post(profile=profile, comment_thread=thread)
            post.hashtags.add(hashtag)
            post.clappers.add(profile)
            factories.Company()

