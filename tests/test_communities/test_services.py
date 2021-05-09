import pytest

from api.community import choices, factories, services
from api.users.factories import ProfileFactory, UserFactory


@pytest.mark.django_db
class TestServices:
    def test_company_clap(self):
        profile = ProfileFactory()
        company = factories.CompanyFactory()
        assert company.clappers.count() == 0
        rv = services.company_clap(company=company, profile=profile)
        assert rv == 1
        rv2 = services.company_clap(company=company, profile=profile)
        assert rv2 == 1
        assert company.clappers.count() == 1

    def test_comment_clap(self):
        thread = factories.ThreadFactory(comments=None)
        comment = factories.CommentFactory(thread=thread)
        profile = ProfileFactory()
        assert comment.clappers.count() == 0
        rv = services.comment_clap(comment=comment, profile=profile)
        assert rv == 1
        rv2 = services.comment_clap(comment=comment, profile=profile)
        assert rv2 == 1
        assert comment.clappers.count() == 1

    def test_create_revision(self):
        profile = ProfileFactory()
        company = factories.CompanyFactory()
        revision = services.create_revision(
            company=company, created_by=profile, name="X"
        )
        assert revision.company == company
        assert revision.name == "X"

    def test_create_comment(self):
        profile = ProfileFactory()
        text = "xxx"
        thread = factories.ThreadFactory(comments=None)
        assert thread.comments.count() == 0

        comment = services.create_comment(profile=profile, text=text, thread=thread)
        assert thread.comments.count() == 1
        assert comment.text == text
        assert comment.profile == profile

        services.create_comment(profile=profile, text=text, thread=thread)
        assert thread.comments.count() == 2

    def test_can_create_company(self):
        user = UserFactory(groups=["editors"])
        profile = ProfileFactory(user=user)

        assert services.can_create_company(profile)

        user2 = UserFactory(groups=[])
        profile2 = ProfileFactory(user=user2)

        assert services.can_create_company(profile2)

        for _ in range(services.MAX_UNMODERATED_CHANGES):
            factories.CompanyFactory(
                created_by=profile2, status=choices.ModerationStatus.UNMODERATED.name
            )
        assert not services.can_create_company(profile2)

    def test_can_create_revision(self):
        user = UserFactory(groups=["editors"])
        profile = ProfileFactory(user=user)

        assert services.can_create_revision(profile)

        user2 = UserFactory(groups=[])
        profile2 = ProfileFactory(user=user2)

        assert services.can_create_revision(profile2)

        for _ in range(services.MAX_UNMODERATED_CHANGES):
            factories.CompanyFactory(
                current_revision__created_by=profile2,
                current_revision__status=choices.ModerationStatus.UNMODERATED.name,
            )

        assert not services.can_create_revision(profile2)
