import pytest
from api.users.factories import ProfileFactory
from api.community import factories, services, selectors


@pytest.mark.django_db
class TestSelectors:
    def test_annotated_company(self):
        profile_1 = ProfileFactory()
        profile_2 = ProfileFactory()
        company_1 = factories.CompanyFactory()
        company_2 = factories.CompanyFactory()
        assert company_1.clappers.count() == company_2.clappers.count() == 0
        assert services.company_clap(company=company_1, profile=profile_1) == 1
        assert services.company_clap(company=company_2, profile=profile_2) == 1

        companies_1 = selectors.get_companies_annotated(profile_id=profile_1.id)
        assert companies_1.all()[0].user_did_clap is True
        assert companies_1.all()[1].user_did_clap is False
        companies_2 = selectors.get_companies_annotated(profile_id=profile_2.id)
        assert companies_2.all()[0].user_did_clap is False
        assert companies_2.all()[1].user_did_clap is True

    def test_annotated_comments(self):
        thread = factories.ThreadFactory()

        profile_1 = ProfileFactory()
        profile_2 = ProfileFactory()
        comment_1 = factories.CommentFactory(thread=thread)
        comment_2 = factories.CommentFactory(thread=thread)
        assert comment_1.clappers.count() == comment_2.clappers.count() == 0
        assert services.comment_clap(comment=comment_1, profile=profile_1) == 1
        assert services.comment_clap(comment=comment_2, profile=profile_2) == 1

        comments_1 = selectors.get_thread_comments_annotated(
            thread_id=thread.id, profile_id=profile_1.id
        )
        assert comments_1.all()[0].user_did_clap is True
        assert comments_1.all()[1].user_did_clap is False

        comments_2 = selectors.get_thread_comments_annotated(
            thread_id=thread.id, profile_id=profile_2.id
        )
        assert comments_2.all()[0].user_did_clap is False
        assert comments_2.all()[1].user_did_clap is True
