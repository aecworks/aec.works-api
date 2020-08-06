import pytest
from django.core.exceptions import PermissionDenied
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

    def test_edit_post(self):
        post = factories.PostFactory()
        updated_post = services.update_post(
            profile=post.profile, slug=post.slug, title="x", body="x", hashtag_names=[]
        )
        assert updated_post.title == "x"

    def test_edit_permissions(self):
        profile = ProfileFactory()
        post = factories.PostFactory()
        with pytest.raises(PermissionDenied):
            services.update_post(
                profile=profile, slug=post.slug, title="x", body="x", hashtag_names=[]
            )
        profile.user.is_staff = True
        profile.save()
        updated_post = services.update_post(
            profile=profile, slug=post.slug, title="x", body="x", hashtag_names=[]
        )
        assert updated_post.title == "x"

    def test_edit_company(self):
        profile = ProfileFactory()
        company = factories.CompanyFactory()
        updated_post = services.update_company(
            company=company, profile=profile, validated_data={"name": "x"}
        )
        assert updated_post.name == "x"
