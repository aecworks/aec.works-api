from datetime import timedelta

from django.db import models as m
from django.utils import timezone

from .models import (
    Comment,
    Company,
    CompanyRevision,
    CompanyRevisionHistory,
    Hashtag,
    Thread,
)


def get_comments():
    return Comment.objects.select_related("profile__avatar", "profile__user").all()


def get_thread(*, id):
    return Thread.objects.get(id=id)


def get_recent_comments(days_back=7):
    now = timezone.now()
    recent = now - timedelta(days=days_back)
    return Comment.objects.filter(created_at__range=[recent, now]).all()


def get_thread_comments(*, thread_id):
    return get_comments().filter(thread_id=thread_id)


def get_company(**kwargs):
    return Company.objects.get(**kwargs)


def get_companies(prefetch=True):
    # TODO separate revisions
    qs = Company.objects.all()
    if prefetch:
        qs = qs.select_related(
            "thread",
            "current_revision__logo",
            "current_revision__cover",
            "current_revision__created_by__avatar",
            "current_revision__created_by__user",
        ).prefetch_related("current_revision__hashtags")
    return qs


def get_company_claps():
    return Company.clappers.through.objects.all()


def query_multi_hashtag(qs, hashtag_slugs):
    # Achieve case insensitive __in using regex:
    reg_pat = f"({'|'.join(hashtag_slugs)})"
    qs_with_one_of = qs.filter(current_revision__hashtags__slug__iregex=reg_pat)
    qs_with_both = qs_with_one_of.annotate(
        n_matches=m.Count("current_revision__hashtags", distinct=True)
    ).filter(n_matches=len(hashtag_slugs))
    return qs_with_both


def query_posts(qs, query, hashtag_slugs):
    if hashtag_slugs:
        qs = query_multi_hashtag(qs, hashtag_slugs)
    if query:
        filters = m.Q(title__icontains=query) | m.Q(body__icontains=query)
        qs = qs.filter(filters)
    return qs


def filter_companies(qs, search, hashtag_slugs, status):
    if hashtag_slugs:
        qs = query_multi_hashtag(qs, hashtag_slugs)
    if search:
        qs = qs.filter(current_revision__name__icontains=search)
    if status:
        qs = qs.filter(status=status)
    return qs


def get_revisions(prefetch=True):
    qs = CompanyRevision.objects
    if prefetch:
        qs = qs.select_related("company", "created_by").prefetch_related("hashtags")
    return qs.all()


def get_revision_history(company, prefetch=True):
    qs = CompanyRevisionHistory.objects
    if prefetch:
        qs = qs.select_related("revision__created_by__user", "created_by__user")
    return qs.filter(revision__company=company)


def get_hashtags():
    return Hashtag.objects.all()
