import pytest

from api.community import factories as f
from api.webhooks.services import is_add_article, resolve_company

# TODO: test view


@pytest.mark.django_db
def test_resolve_company():
    c = f.CompanyFactory(slug="aec")
    rev = f.CompanyRevisionFactory(company=c, name="AEC", twitter="aec_works")
    assert resolve_company("add http://x/a to @aec_works", "aec_works") == c
    assert resolve_company("add http://x/a to @Aec_Works", "Aec_Works") == c
    assert resolve_company("add http://x/a to @.aec", "") == c
    assert resolve_company("add http://x/a to @.Aec", "") == c
    assert not resolve_company("add http://x/a to @xxx", "")
    assert not resolve_company("add http://x/a to @xxx", "xxx")


def test_is_add_article():
    assert is_add_article("Add https://t.co/aEQasd to @aec_works")
    assert not is_add_article("Add this")
