import pytest
from django.core.exceptions import PermissionDenied
from api.users.factories import ProfileFactory
from api.community import factories, services


@pytest.mark.django_db
class TestServices:
    def test_post_clap(self):
        profile = ProfileFactory()
        post = factories.PostFactory()
        assert post.clappers.count() == 0
        rv = services.post_clap(post=post, profile=profile)
        assert rv == 1
        rv2 = services.post_clap(post=post, profile=profile)
        assert rv2 == 1
        assert post.clappers.count() == 1

    def test_comment_clap(self):
        thread = factories.ThreadFactory()
        comment = factories.CommentFactory(thread=thread)
        profile = ProfileFactory()
        assert comment.clappers.count() == 0
        rv = services.comment_clap(comment=comment, profile=profile)
        assert rv == 1
        rv2 = services.comment_clap(comment=comment, profile=profile)
        assert rv2 == 1
        assert comment.clappers.count() == 1

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

    def test_create_revision(self):
        profile = ProfileFactory()
        company = factories.CompanyFactory()
        revision = services.create_revision(
            company=company, profile=profile, validated_data={"name": "x"}
        )
        assert revision.company == company
        assert revision.name == "x"

    def test_apply_revision(self):
        profile = ProfileFactory()
        company = factories.CompanyFactory()
        rev = factories.CompanyRevisionFactory(company=company)

        updated_company = services.apply_revision(revision=rev, profile=profile)
        last_revision = updated_company.last_revision

        assert last_revision == rev
        assert last_revision.company == company
        assert last_revision.approved_by == profile
        assert last_revision.applied is True
