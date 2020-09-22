import re
from api.community.models import Company
from api.community.selectors import get_company
from api.community.services import create_company_article


class TweetCompanyReferenceNotFound(Exception):
    ...


def create_article_from_tweet(*, url, text, mentioned, hashtags, profile):
    """
    The expected tweet format is:

    >>> "Checkout this article https://url @company #aecworks"

    This tweet will add link url to company with twitter handle.
    If a company does not have a twiter account, `@.slug` can be used to reference it by
    its slug
    """
    if mentioned:
        get_kwargs = dict(twitter_handle__iexact=mentioned)
    else:
        match = re.search(r"@\.(\w+)", text)
        if not match:
            raise TweetCompanyReferenceNotFound("no company reference found")
        get_kwargs = dict(slug=match.group(1))

    try:
        company = get_company(**get_kwargs)
    except Company.DoesNotExist:
        raise TweetCompanyReferenceNotFound("company reference not found")

    return create_company_article(company=company, url=url, profile=profile)
