from typing import List
from django.db import transaction
from django.core.exceptions import PermissionDenied

from .models import Comment, Hashtag, Post, Thread


def post_clap(*, post, profile):
    post.clappers.add(profile)
    return post.clappers.count()


def create_thread_comment(*, profile, thread, text):
    return Comment.objects.create(profile=profile, thread=thread, text=text)


@transaction.atomic
def create_post(*, profile, title: str, body: str, hashtag_names: List[str]):
    hashtags = Hashtag.objects.filter(slug__in=hashtag_names)
    thread = Thread.objects.create()
    post = Post.objects.create(profile=profile, title=title, body=body, thread=thread)
    post.hashtags.set(hashtags)
    return post


@transaction.atomic
def update_post(*, profile, slug: str, title: str, body: str, hashtag_names: List[str]):
    hashtags = Hashtag.objects.filter(slug__in=hashtag_names)
    post = Post.objects.get(slug=slug)
    if post.profile == profile or profile.user.is_staff:
        Post.objects.filter(id=post.id).update(title=title, body=body)
        post.hashtags.set(hashtags)
        post.refresh_from_db()
        return post
    raise PermissionDenied()
