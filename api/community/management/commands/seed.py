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
        # hashtag = factories.Hashtag()

        comment = factories.Comment(profile=profile)
        factories.Comment(profile=profile, parent=comment)
        factories.Comment(profile=profile, parent=comment)
        factories.Comment(profile=profile, parent=comment)
        factories.Comment(profile=profile, parent=comment)
        factories.Comment(profile=profile, parent=comment)
        factories.Comment(profile=profile, parent=comment)
        factories.Comment(profile=profile, parent=comment)
        factories.Comment(profile=profile, parent=comment)
        factories.Comment(profile=profile, parent=comment)
        factories.Comment(profile=profile, parent=comment)
        factories.Comment(profile=profile, parent=comment)
        factories.Comment(profile=profile, parent=comment)

        # post = factories.Post(profile=profile, root_comment=comment)
        # post.hashtags.add(hashtag)
        # post.clappers.add(profile)

        # factories.Company()

