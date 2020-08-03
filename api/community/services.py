from typing import List
from django.db import transaction
from django.core.exceptions import PermissionDenied

from .models import Comment, Hashtag, Post, Thread


def post_clap(*, post, profile):
    post.clappers.add(profile)
    return post.clappers.count()


def create_thread_comment(*, profile, thread, text):
    return Comment.objects.create(profile=profile, thread=thread, text=text)


def get_or_create_hashtags(hashtag_names: List[str]):
    return [
        Hashtag.objects.filter(slug=n).first() or Hashtag.objects.create(slug=n)
        for n in hashtag_names
    ]


@transaction.atomic
def create_post(*, profile, title: str, body: str, hashtag_names: List[str]):
    hashtags = get_or_create_hashtags(hashtag_names)
    thread = Thread.objects.create()
    post = Post.objects.create(profile=profile, title=title, body=body, thread=thread)
    post.hashtags.set(hashtags)
    return post


@transaction.atomic
def update_post(*, profile, slug: str, title: str, body: str, hashtag_names: List[str]):
    post = Post.objects.get(slug=slug)
    if not post.profile == profile and not profile.user.is_staff:
        raise PermissionDenied(f"profile '{profile.name}' cannot edit this post")

    hashtags = get_or_create_hashtags(hashtag_names)
    Post.objects.filter(id=post.id).update(title=title, body=body)
    post.hashtags.set(hashtags)
    post.refresh_from_db()
    return post
