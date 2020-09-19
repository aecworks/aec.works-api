import pytest
from api.users.factories import ProfileFactory
from api.community.factories import CompanyFactory
from api.webhooks.services import (
    create_article_from_tweet,
    TweetCompanyReferenceNotFound,
)


@pytest.mark.django_db
def test_article_from_tweet():
    company = CompanyFactory(twitter_handle="xxx")
    profile = ProfileFactory()
    url = "https://abc.com"
    article = create_article_from_tweet(
        url=url,
        mentioned="xxx",
        text="See this @xxx",
        hashtags="abc,def",
        profile=profile,
    )
    assert article.company == company
    assert article.url == url
    assert article.created_by == profile


@pytest.mark.django_db
def test_article_from_tweet_using_slug():
    company = CompanyFactory(name="zzz")
    profile = ProfileFactory()
    article = create_article_from_tweet(
        url="https://abc.com",
        mentioned="",
        text="See @.zzz",
        hashtags="",
        profile=profile,
    )
    assert article.company == company


@pytest.mark.django_db
def test_article_from_tweet_using_no_match():
    profile = ProfileFactory()
    with pytest.raises(TweetCompanyReferenceNotFound):
        create_article_from_tweet(
            url="https://a.b",
            text="Checkout @nonexistent",
            mentioned="nonexistent",
            hashtags="",
            profile=profile,
        )
    with pytest.raises(TweetCompanyReferenceNotFound):
        create_article_from_tweet(
            url="https://a.b",
            mentioned="",
            text="Checkout @.nonexistent",
            hashtags="",
            profile=profile,
        )