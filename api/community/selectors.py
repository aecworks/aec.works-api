from datetime import timedelta, date
from django.db.models import Count, Q
from .models import Company, CompanyRevision, Comment, Post, Hashtag, Thread


def get_comments():
    return Comment.objects.select_related("profile__user").with_counts().all()


def get_thread(*, id):
    return Thread.objects.get(id=id)


def get_recent_comments(days_back=7):
    today = date.today()
    recent = today - timedelta(days=days_back)
    tomorrow = today + timedelta(days=1)
    return (
        Comment.objects.filter(created_at__range=[recent, tomorrow]).with_counts().all()
    )


def get_thread_comments(*, thread_id):
    return get_comments().filter(level=0, thread_id=thread_id)


def get_comment_children(*, parent_id):
    return get_comments().filter(parent_id=parent_id)


def get_company(**kwargs):
    return Company.objects.get(**kwargs)


def get_companies():
    return (
        Company.objects.select_related("created_by", "thread")
        .prefetch_related("hashtags", "articles")
        .with_counts()
        .all()
    )


def query_multi_hashtag(qs, hashtag_slugs):
    # Achieve case insensitive __in using regex:
    reg_pat = f"({'|'.join(hashtag_slugs)})"
    qs_with_one_of = qs.filter(hashtags__slug__iregex=reg_pat)
    # qs_with_one_of = qs.filter(hashtags__slug__in=hashtag_slugs)
    qs_with_both = qs_with_one_of.annotate(
        n_matches=Count("hashtags", distinct=True)
    ).filter(n_matches=len(hashtag_slugs))
    return qs_with_both


def query_posts(qs, query, hashtag_slugs):
    if hashtag_slugs:
        qs = query_multi_hashtag(qs, hashtag_slugs)
    if query:
        filters = Q(title__icontains=query) | Q(body__icontains=query)
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
        Post.objects.select_related("profile__user")
        .prefetch_related("hashtags", "companies", "thread__comments")
        .with_counts()
        .all()
    )
