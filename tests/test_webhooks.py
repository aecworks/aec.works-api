import pytest

from api.community.factories import CompanyFactory
from api.webhooks.services import is_add_article, resolve_company

# TODO: test view


@pytest.mark.django_db
def test_resolve_company():
    company = CompanyFactory(slug="aec", twitter="aec_works")
    assert resolve_company("add http://x/a to @aec_works", "aec_works") == company
    assert resolve_company("add http://x/a to @Aec_Works", "Aec_Works") == company
    assert resolve_company("add http://x/a to @.aec", "") == company
    assert resolve_company("add http://x/a to @.Aec", "") == company
    assert not resolve_company("add http://x/a to @xxx", "")
    assert not resolve_company("add http://x/a to @xxx", "xxx")


def test_is_add_article():
    assert is_add_article("Add https://t.co/aEQasd to @aec_works")
    assert not is_add_article("Add this")
