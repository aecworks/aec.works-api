from django.db import models
from .models import Company, Comment, Post, Hashtag


def get_comments():
    return (
        Comment.objects.select_related("profile")
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
            "editor", "comment_thread", "approved_by", "replaced_by", "revision_of"
        )
        .prefetch_related("hashtags")
        .annotate(claps=models.Count("clappers"))
        .all()
    )


def get_hashtags():
    return Hashtag.objects.all()


def get_posts():
    return (
        Post.objects.select_related("profile")
        .prefetch_related("hashtags", "companies", "comment_thread__comments")
        .annotate(clap_count=models.Count("clappers", distinct=True))
        .all()
    )
