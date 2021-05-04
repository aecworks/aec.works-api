from unittest import mock

import pytest

from api.community import factories as f
from api.webhooks.services import is_add_article, resolve_company

# TODO: test view


@pytest.mark.django_db
def test_resolve_company():
    c = f.CompanyFactory(
        slug="aec", current_revision__twitter="aec_works", current_revision__name="AEC"
    )
    assert resolve_company("add http://x/a to @aec_works", "aec_works") == c
    assert resolve_company("add http://x/a to @Aec_Works", "Aec_Works") == c
    assert resolve_company("add http://x/a to @.aec", "") == c
    assert resolve_company("add http://x/a to @.Aec", "") == c
    assert not resolve_company("add http://x/a to @xxx", "")
    assert not resolve_company("add http://x/a to @xxx", "xxx")


def test_is_add_article():
    assert is_add_article("Add https://t.co/aEQasd to @aec_works")
    assert not is_add_article("Add this")


@mock.patch("api.community.services.get_og_data")
def test_post_webhook(m_get_og_data, auth_client, token_auth_client):

    company = f.CompanyFactory(current_revision__twitter="ABC")
    assert company.articles.count() == 0

    m_get_og_data.return_value = {"key": "value"}

    URL = "https://www.latimes.com/entertainment-arts/story/2021-03-05/new-city-program-brings-high-design-concepts-to-granny-flat"
    payload = {
        "mentioned": "ABC",
        "text": "Add https://fake.com to @ABC https://fake.com",
        "url": URL,
    }
    resp = token_auth_client.post("/webhooks/twitter/", payload, format="json")
    assert resp.status_code == 201
    company.refresh_from_db()
    assert company.articles.count() == 1
    assert m_get_og_data.called

    assert company.articles.first().url == URL
    assert company.articles.first().opengraph_data == {"key": "value"}
