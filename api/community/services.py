from typing import List
from math import log
from datetime import timedelta
from django.db import transaction
from django.utils.text import slugify
from django.core.exceptions import PermissionDenied

from api.common.utils import update_instance
from .models import (
    Comment,
    Hashtag,
    Post,
    Thread,
    Company,
    CompanyRevision,
)

updatable_attributes = [
    "name",
    "description",
    "website",
    "location",
    "twitter_handle",
    "crunchbase_id",
    "logo_url",
    "cover_url",
    "hashtags",
]


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


def create_comment(*, profile, text, **parent_kwarg) -> Comment:
    # must include parent=, parent_id, thread, or thread_id
    return Comment.objects.create(profile=profile, text=text, **parent_kwarg)


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
def create_company(*, profile, validated_data) -> Company:
    hashtag_names = validated_data.pop("hashtags", [])
    hashtags = get_or_create_hashtags(hashtag_names)
    company = Company.objects.create(created_by=profile, **validated_data)
    company.hashtags.set(hashtags)
    return company


@transaction.atomic
def create_revision(*, company, profile, validated_data) -> CompanyRevision:
    hashtag_names = validated_data.pop("hashtags", [])
    hashtags = get_or_create_hashtags(hashtag_names)
    revision = CompanyRevision.objects.create(
        company=company, created_by=profile, **validated_data
    )
    revision.hashtags.set(hashtags)
    return revision


@transaction.atomic
def apply_revision(*, revision, profile):
    update_data = {k: v for k, v in vars(revision).items() if k in updatable_attributes}
    update_data["last_revision"] = revision
    update_instance(revision.company, update_data)

    revision.approved_by = profile
    revision.applied = True
    revision.save()
