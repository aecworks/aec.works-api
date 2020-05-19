from django.db import models

from api.common.lookups import Floor
from .models import Company, Comment, Post, Hashtag, Thread


def get_comments():
    return (
        Comment.objects.select_related("profile__user")
        .annotate(
            clap_count=models.Count("clappers", distinct=True),
            replies_count=models.Count("replies", distinct=True),
        )
        .all()
    )


def get_thread_comments(*, thread_id):
    return get_comments().filter(level=0, thread_id=thread_id)


def get_comment_children(*, parent_id):
    return get_comments().filter(parent_id=parent_id)


def get_companies():
    return (
        Company.objects.select_related(
            "editor", "thread", "approved_by", "replaced_by", "revision_of"
        )
        .prefetch_related("hashtags")
        .annotate(claps=models.Count("clappers"))
        .all()
    )


def get_hashtags():
    return Hashtag.objects.all()


def get_posts():
    return (
        Post.objects.select_related("profile__user")
        .prefetch_related("hashtags", "companies", "thread__comments")
        .annotate(clap_count=models.Count("clappers", distinct=True))
        .all()
    )


def get_posts_with_comment_count():
    # See
    # https://stackoverflow.com/questions/20139372/django-queryset-attach-or-annotate-related-object-field/47725075

    # this query reproduces the get_descendant_count() logic for each top level comment
    # https://django-mptt.readthedocs.io/en/latest/models.html#get-descendant-count
    threads = Thread.objects.filter(id=models.OuterRef("thread_id")).annotate(
        comment_count=models.Sum(
            Floor((models.F("comments__rght") - models.F("comments__lft") - 1) / 2)
        )
    )
    # Reuse pre-loaded posts qs and annotate comment.
    # Comment count subquery includes "descendent count", but the top level comment
    # itself is not included, so we add that on top.
    return (
        get_posts()
        .annotate(
            comment_count=models.Subquery(
                threads.values("comment_count")[:1], output_field=models.IntegerField()
            )
        )
        .annotate(
            comment_count=models.F("comment_count")
            + models.Count("thread__comments", distinct=True)
        )
    )
