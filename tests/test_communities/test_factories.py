import pytest

from api.community import factories as f
from api.users.factories import ProfileFactory


@pytest.mark.django_db
class TestFactories:
    def test_company_factory(self):
        h1 = f.HashtagFactory(slug="H")
        c1 = f.CompanyFactory(
            slug="slug", current_revision__twitter="T", current_revision__hashtags=[h1]
        )
        assert c1.slug == "slug"
        assert c1.current_revision
        assert c1.current_revision.name == "Slug"
        assert c1.current_revision.twitter == "T"
        assert c1.current_revision.hashtags.first().slug == "H"

    def test_company_revision_factory(self):
        co = f.CompanyFactory(slug="Name")
        assert not co.current_revision
        rev = f.CompanyRevisionFactory(company=co, name="ABC")
        assert co.slug == "Name"
        assert rev.name == "ABC"
        assert co.current_revision is None
        assert rev in co.revisions.all()

    def test_company_revision_history_factory(self):
        profile = ProfileFactory()
        co = f.CompanyFactory(current_revision__name="X")
        assert co.current_revision
        hist = f.CompanyRevisionHistoryFactory(
            created_by=profile, revision=co.current_revision
        )
        assert hist.created_by == profile
        assert hist.revision == co.current_revision

    def test_comment_factory(self):
        profile = ProfileFactory()
        co = f.CommentFactory(text="text", profile=profile)
        assert co.text == "text"
        assert co.profile == profile
        assert co.thread

        thread = f.ThreadFactory()
        co = f.CommentFactory(thread=thread)
        assert co.thread == thread

    def test_thread_factory(self):
        co = f.ThreadFactory(comments=None)
        assert co.comments.count() == 0

        co = f.ThreadFactory(comments__text="x")
        assert co.comments.first().text == "x"
