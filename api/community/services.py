from typing import List
from math import log
from datetime import timedelta
from django.db import transaction
from django.utils.text import slugify
from django.core.exceptions import PermissionDenied

from api.common.utils import update_instance
from .models import Comment, Hashtag, Post, Thread, Company


def bump_hot_datetime(post, clap_count):
    # Each Clap bumps up 1/4 day or 6 hours
    bump = log(25 * clap_count + 1, 2) / 3
    time_bump = timedelta(days=bump)
    # >>> log(25 * 0 + 1, 2) / 3 => 0.0
    # >>> log(25 * 1 + 1, 2) / 3 => 1.5
    # >>> log(25 * 5 + 1, 2) / 3 => 2.3
    # >>> log(25 * 20 + 1, 2) / 3 => 2.9
    # >>> log(25 * 100 + 1, 2) / 3 => 3.7
    post.hot_datetime = post.created_at + time_bump
    post.save()


def comment_clap(*, comment, profile) -> int:
    comment.clappers.add(profile)
    return comment.clappers.count()


def post_clap(*, post, profile) -> int:
    post.clappers.add(profile)
    clap_count = post.clappers.count()
    bump_hot_datetime(post, clap_count)
    return clap_count


def create_thread_comment(*, profile, thread, text) -> Comment:
    return Comment.objects.create(profile=profile, thread=thread, text=text)


def get_or_create_hashtag(hashtag_name: str) -> Hashtag:
    slug = slugify(hashtag_name).replace("-", "")
    return Hashtag.objects.filter(slug=slug).first() or Hashtag.objects.create(
        slug=slug
    )


def get_or_create_hashtags(hashtag_names: List[str]) -> List[Hashtag]:
    return [get_or_create_hashtag(name) for name in hashtag_names]


@transaction.atomic
def create_post(*, profile, title: str, body: str, hashtag_names: List[str]) -> Post:
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


@transaction.atomic
def update_company(*, company, profile, validated_data) -> Company:
    hashtag_names = validated_data.get("hashtags", [])
    validated_data["hashtags"] = get_or_create_hashtags(hashtag_names)
    validated_data["profile_id"] = profile.id
    updated_company = update_instance(company, validated_data)
    return updated_company
