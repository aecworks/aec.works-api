from datetime import timedelta
from django.utils import timezone
from django.db import models as m
from .models import Company, CompanyRevision, Comment, Post, Hashtag, Thread


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


def get_thread_comments_annotated(*, thread_id, profile_id=-1):
    return (
        get_comments()
        .filter(thread_id=thread_id)
        .annotate(
            user_did_clap=m.Case(
                m.When(clappers__id__contains=profile_id, then=True),
                default=False,
                output_field=m.BooleanField(),
            ),
        )
    )


def get_company(**kwargs):
    return Company.objects.get(**kwargs)


def get_companies():
    qs = (
        Company.objects.select_related("logo", "cover")
        .prefetch_related("hashtags", "articles")
        .all()
    )
    return qs


def get_companies_annotated(profile_id=-1):
    """
    Annotates Companies with "thread_size" (comment count)
    and `user_did_clap` indicating if provided profile has clapped
    """
    return get_companies().annotate(
        thread_size=m.Count("thread__comments", distinct=True),
        user_did_clap=m.Case(
            m.When(clappers__id__contains=profile_id, then=True),
            default=False,
            output_field=m.BooleanField(),
        ),
    )


def get_company_claps():
    return Company.clappers.through.objects.all()


def query_multi_hashtag(qs, hashtag_slugs):
    # Achieve case insensitive __in using regex:
    reg_pat = f"({'|'.join(hashtag_slugs)})"
    qs_with_one_of = qs.filter(hashtags__slug__iregex=reg_pat)
    qs_with_both = qs_with_one_of.annotate(
        n_matches=m.Count("hashtags", distinct=True)
    ).filter(n_matches=len(hashtag_slugs))
    return qs_with_both


def query_posts(qs, query, hashtag_slugs):
    if hashtag_slugs:
        qs = query_multi_hashtag(qs, hashtag_slugs)
    if query:
        filters = m.Q(title__icontains=query) | m.Q(body__icontains=query)
        qs = qs.filter(filters)
    return qs


def query_companies(qs, query, hashtag_slugs):
    if hashtag_slugs:
        qs = query_multi_hashtag(qs, hashtag_slugs)
    if query:
        qs = qs.filter(name__icontains=query)
    return qs


def get_revisions():
    return (
        CompanyRevision.objects.select_related("company", "created_by")
        .prefetch_related("hashtags")
        .all()
    )


def get_hashtags():
    return Hashtag.objects.with_counts().all()


def get_posts():
    return (
        Post.objects.select_related("profile__user", "profile__avatar")
        .prefetch_related("hashtags", "companies", "thread__comments")
        .all()
    )
