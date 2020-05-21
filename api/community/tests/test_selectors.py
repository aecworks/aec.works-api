import pytest
from api.users.factories import ProfileFactory
from api.community import selectors, factories

# from django.test import TestCase


@pytest.mark.django_db
class TestCommunitySelector:
    def test_get_comments(self):
        profile = ProfileFactory()
        thread = factories.Thread()
        c1 = factories.Comment(thread=thread)
        factories.Comment(parent=c1)
        factories.Comment(parent=c1)
        c1.clappers.add(profile)

        comments = selectors.get_comments()

        assert comments[0].clap_count == 1
        assert comments[1].clap_count == 0
        assert comments[2].clap_count == 0
