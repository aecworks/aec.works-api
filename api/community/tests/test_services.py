import pytest

from api.users.factories import ProfileFactory
from api.community import factories, services


@pytest.mark.django_db
class TestServices:
    def test_post_clap(self):
        post = factories.PostFactory()
        profile = ProfileFactory()
        rv = services.post_clap(post=post, profile=profile)
        assert rv == 1
        rv2 = services.post_clap(post=post, profile=profile)
        assert rv2 == 1
        assert post.clappers.count() == 1
