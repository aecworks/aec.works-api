from typing import List
from math import log
from datetime import timedelta
from django.db import transaction
from django.core.exceptions import PermissionDenied
from opengraph.opengraph import OpenGraph

from api.community.choices import PostBanner
from api.common.utils import update_instance, to_hashtag
from .models import (
    Article,
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


def company_clap(*, company, profile) -> int:
    company.clappers.add(profile)
    clap_count = company.clappers.count()
    # bump_hot_datetime(post, clap_count)
    return clap_count


def post_clap(*, post, profile) -> int:
    post.clappers.add(profile)
    clap_count = post.clappers.count()
    bump_hot_datetime(post, clap_count)
    return clap_count


def create_comment(*, profile, text, **parent_kwarg) -> Comment:
    # must include parent=, parent_id, thread, or thread_id
    return Comment.objects.create(profile=profile, text=text, **parent_kwarg)


def get_or_create_hashtag(hashtag_name: str) -> Hashtag:
    slug = to_hashtag(hashtag_name)
    return Hashtag.objects.filter(slug__iexact=slug).first() or Hashtag.objects.create(
        slug=slug
    )


def get_or_create_hashtags(hashtag_names: List[str]) -> List[Hashtag]:
    return [get_or_create_hashtag(name) for name in hashtag_names]


def generate_post_banner(profile):
    if profile.posts.count() == 0:
        return PostBanner.FIRST_POST.value
    return ""


@transaction.atomic
def create_post(*, profile, title: str, body: str, hashtag_names: List[str]) -> Post:
    hashtags = get_or_create_hashtags(hashtag_names)
    thread = Thread.objects.create()
    banner = generate_post_banner(profile)
    post = Post.objects.create(
        profile=profile, title=title, body=body, thread=thread, banner=banner
    )
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
    update_data = {attr: getattr(revision, attr) for attr in updatable_attributes}
    update_data["last_revision"] = revision
    update_instance(revision.company, update_data)

    revision.approved_by = profile
    revision.applied = True
    revision.save()


def create_company_article(*, company, url, profile):
    article = Article.objects.create(url=url, company=company, created_by=profile)
    og_article = OpenGraph(url=url)
    if og_article.is_valid():
        tags = [
            "site_name",
            "type",
            "title",
            "description",
            "image",
            "image:alt",
            "image:height",
            "image:width",
        ]
        article.opengraph_data = {k: v for k, v in og_article.items() if k in tags}
        article.save()
    return article


def parse_hashtag_query(query: str):
    if not query:
        return []
    return query.split(",")
