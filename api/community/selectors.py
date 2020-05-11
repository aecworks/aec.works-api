from django.db import models
from .models import Company, Comment, Post, Hashtag


def get_root_comments():
    return (
        Comment.objects.annotate(
            claps=models.Count("clappers", distinct=True),
            replies_count=models.Count("replies", distinct=True),
        )
        .filter(level=0)
        .all()
    )


def get_comments(pk):
    return (
        Comment.objects.get(pk=pk)
        .get_children()
        .select_related("profile")
        .annotate(
            claps=models.Count("clappers", distinct=True),
            replies_count=models.Count("replies", distinct=True),
        )
        .all()
    )


def get_companies():
    return (
        Company.objects.select_related(
            "editor", "root_comment", "approved_by", "replaced_by", "revision_of"
        )
        .prefetch_related("hashtags")
        .annotate(claps=models.Count("clappers"))
        .all()
    )


def get_hashtags():
    return Hashtag.objects.all()


def get_posts():
    return (
        Post.objects.select_related("profile", "root_comment")
        .prefetch_related("hashtags", "companies")
        .annotate(claps=models.Count("clappers"))
        .all()
    )
