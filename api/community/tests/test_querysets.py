import pytest
from api.users.factories import ProfileFactory
from api.community import selectors, factories, models

# from django.test import TestCase


@pytest.mark.django_db
class TestQuerysets:
    def test_comment_counts(self):
        profile = ProfileFactory()

        thread = factories.Thread()
        c0 = factories.Comment(thread=thread)
        factories.Comment(parent=c0)
        factories.Comment(parent=c0)
        c0.clappers.add(profile)

        comments = models.Comment.objects.with_counts().all()
        assert comments[0].clap_count == 1
        assert comments[0].reply_count == 2
        assert comments[1].clap_count == 0
        assert comments[2].clap_count == 0

    def test_post_counts(self):
        profile = ProfileFactory()

        thread = factories.Thread()
        post = factories.Post(thread=thread)
        c0 = factories.Comment(thread=thread)
        factories.Comment(parent=c0)
        factories.Comment(parent=c0)
        post.clappers.add(profile)

        post = models.Post.objects.with_counts().all()
        assert post[0].clap_count == 1
        assert post[0].thread_size == 3
