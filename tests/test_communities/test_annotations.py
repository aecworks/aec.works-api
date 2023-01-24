import pytest

from api.community import annotations, factories, selectors, services
from api.users.factories import ProfileFactory


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

        qs_anno_1 = annotations.annotate_company_claps(
            selectors.get_companies(), profile_id=profile_1.id
        )

        assert qs_anno_1.get(id=company_1.id).user_did_clap is True
        assert qs_anno_1.get(id=company_2.id).user_did_clap is False

        qs_anno_2 = annotations.annotate_company_claps(
            selectors.get_companies(), profile_id=profile_2.id
        )
        assert qs_anno_2.get(id=company_1.id).user_did_clap is False
        assert qs_anno_2.get(id=company_2.id).user_did_clap is True

    def test_annotated_company_bug(self):
        """sometimes annotate causes query to return duplicates"""
        profile = ProfileFactory()
        profile_2 = ProfileFactory()
        company = factories.CompanyFactory()
        _ = factories.CompanyFactory()

        services.company_clap(company=company, profile=profile)
        services.company_clap(company=company, profile=profile_2)

        n_annotated = annotations.annotate_comment_claps(
            selectors.get_companies(), profile_id=profile.id
        ).count()
        n_companies = selectors.get_companies().count()
        assert n_annotated == n_companies

    def test_annotated_comments(self):
        thread = factories.ThreadFactory(comments=None)

        profile_1 = ProfileFactory()
        profile_2 = ProfileFactory()
        comment_1 = factories.CommentFactory(thread=thread)
        comment_2 = factories.CommentFactory(thread=thread)
        assert comment_1.clappers.count() == comment_2.clappers.count() == 0
        assert services.comment_clap(comment=comment_1, profile=profile_1) == 1
        assert services.comment_clap(comment=comment_2, profile=profile_2) == 1

        comments_1 = annotations.annotate_comment_claps(
            selectors.get_thread_comments(thread_id=thread.id),
            profile_id=profile_1.id,
        )
        assert comments_1.all()[0].user_did_clap is True
        assert comments_1.all()[1].user_did_clap is False

        comments_2 = annotations.annotate_comment_claps(
            selectors.get_thread_comments(thread_id=thread.id), profile_id=profile_2.id
        )
        assert comments_2.all()[0].user_did_clap is False
        assert comments_2.all()[1].user_did_clap is True

    def test_annotated_comments_annotated(self):
        """sometimes annotate causes query to return duplicates"""
        profile = ProfileFactory()
        profile_2 = ProfileFactory()
        thread = factories.ThreadFactory(comments=None)
        comment = factories.CommentFactory(thread=thread)
        comment_2 = factories.CommentFactory(thread=thread)

        services.comment_clap(comment=comment, profile=profile)
        services.comment_clap(comment=comment_2, profile=profile_2)

        n_annotated = annotations.annotate_comment_claps(
            selectors.get_thread_comments(thread_id=thread.id), profile_id=profile.id
        ).count()
        n_comments = selectors.get_thread_comments(thread_id=thread.id).count()
        assert n_annotated == n_comments
