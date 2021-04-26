import re

from api.community.models import Company
from api.community.services import create_company_article


class TweetCompanyReferenceNotFound(Exception):
    ...


def create_article_from_tweet(*, company, url, profile):
    return create_company_article(company=company, url=url, profile=profile)


def is_add_article(text):
    """
    The expected tweet format is:

    >>> "Add https://url to @company"

    This tweet will add link url to company with twitter handle.
    If a company does not have a twiter account, `@.slug` can be used to reference it by
    its slug
    """
    return bool(re.match(r"add http.+\sto\s@", text, re.IGNORECASE))


def resolve_company(text, mentioned):
    if mentioned:
        get_kwargs = dict(twitter__iexact=mentioned)
    else:
        match = re.search(r"@\.(\w+)", text)
        if not match:
            raise TweetCompanyReferenceNotFound("no company reference found")
        get_kwargs = dict(slug=match.group(1))

    company = Company.objects.filter(**get_kwargs).first()
    return company
