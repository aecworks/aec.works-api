from api.users.factories import ProfileFactory
from api.community import selectors, factories
from django.test import TestCase


class TestCommunitySelector(TestCase):
    def test_get_comments(self):
        profile = ProfileFactory()
        thread = factories.CommentThread()
        c1 = factories.Comment(thread=thread)
        factories.Comment(parent=c1)
        factories.Comment(parent=c1)
        c1.clappers.add(profile)

        comments = selectors.get_comments()
        self.assertEqual(comments[0].clap_count, 1)
        self.assertEqual(comments[1].clap_count, 0)
        self.assertEqual(comments[2].clap_count, 0)
