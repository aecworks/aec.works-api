import pytest

from api.community import choices, factories, selectors


@pytest.mark.django_db
class TestSelectors:
    def test_filter_company_hashtags(self):
        h_1 = factories.HashtagFactory(slug="a")
        h_2 = factories.HashtagFactory(slug="b")

        company_1 = factories.CompanyFactory(name="A")
        company_1.hashtags.set([h_1])
        company_2 = factories.CompanyFactory(name="B")
        company_2.hashtags.set([h_2])
        company_3 = factories.CompanyFactory(
            name="C", status=choices.CompanyStatus.REJECTED.name
        )

        qs = selectors.get_companies()

        rv = selectors.filter_companies(qs, None, ["b"], None)
        assert rv.count() == 1
        assert rv.first().slug == company_2.slug

        rv = selectors.filter_companies(qs, company_2.slug, None, None)
        assert rv.count() == 1
        assert rv.first().slug == company_2.slug

        rv = selectors.filter_companies(
            qs, None, None, choices.CompanyStatus.REJECTED.name
        )
        assert rv.count() == 1
        assert rv.first().slug == company_3.slug
