from . import selectors


def hashtag_last_modified(request) -> str:
    lastmod = selectors.get_hashtags().order_by("updated_at").last()
    return lastmod.updated_at


def company_list_last_modified(request) -> str:
    lastmod = selectors.get_companies(prefetch=False).order_by("updated_at").last()
    return lastmod.updated_at


def company_last_modified(request, slug) -> str:
    company = selectors.get_companies(prefetch=False).filter(slug=slug).first()
    return "" if not company else company.updated_at
