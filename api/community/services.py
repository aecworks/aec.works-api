import logging
from datetime import timedelta
from math import log
from typing import List, NamedTuple, Optional, Tuple

from bs4 import BeautifulSoup
from django.core.exceptions import PermissionDenied
from django.db import transaction
from django.utils.text import slugify

from api.common.utils import get_og_data, to_hashtag, update_instance
from api.community.choices import ModerationStatus, PostBanner
from api.images.models import ImageAsset
from api.images.services import create_image_asset, create_image_file_from_data_uri
from api.users.models import Profile
from api.users.services import user_is_editor

from .models import Article, Comment, Company, CompanyRevision, Hashtag, Post, Thread

logger = logging.getLogger(__name__)

updatable_attributes = [
    "name",
    "description",
    "website",
    "location",
    "twitter",
    "crunchbase_id",
    "logo",
    "cover",
    "hashtags",
]


class CompanyRevisionAttributes(NamedTuple):
    name: str
    description: str
    website: str
    location: str
    twitter: str
    crunchbase_id: str
    logo: Optional[str]
    cover: Optional[str]
    hashtags: List[Hashtag]


class CompanyAttributes(NamedTuple):
    name: str
    description: str
    website: str
    location: str
    twitter: str
    crunchbase_id: str
    status: str
    logo: Optional[str]
    cover: Optional[str]


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
    return comment.clap_count


def company_clap(*, company, profile) -> int:
    company.clappers.add(profile)
    # bump_hot_datetime(post, clap_count)
    return company.clap_count


def post_clap(*, post, profile) -> int:
    post.clappers.add(profile)
    post.clap_count = post.clappers.count()
    post.save()
    bump_hot_datetime(post, post.clap_count)
    return post.clap_count


@transaction.atomic
def create_comment(*, profile, text, thread) -> Comment:
    comment = Comment.objects.create(profile=profile, text=text, thread=thread)
    return comment


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


def extract_image_assets(body: str, profile) -> Tuple[str, List[ImageAsset]]:
    """ Given a html body, create one `ImageAsset` for each <img>
    Returns an updated body and a list of generated `ImageAsset` objects
    """
    soup = BeautifulSoup(body, "html.parser")
    img_assets = []
    for img_tag in soup.find_all("img"):
        img_file = create_image_file_from_data_uri(img_tag["src"])
        img_asset = create_image_asset(img_file=img_file, profile=profile)
        img_tag["src"] = img_asset.file.url
        img_assets.append(img_asset)
    return str(soup), img_assets


@transaction.atomic
def create_post(*, profile, title: str, body: str, hashtag_names: List[str]) -> Post:
    hashtags = get_or_create_hashtags(hashtag_names)
    thread = Thread.objects.create()
    banner = generate_post_banner(profile)
    updated_body, imgs = extract_image_assets(body, profile)
    cover_img = None if not imgs else imgs[0]
    post = Post.objects.create(
        profile=profile,
        title=title,
        body=updated_body,
        cover=cover_img,
        thread=thread,
        banner=banner,
    )
    post.hashtags.set(hashtags)
    if imgs:
        post.images.set(imgs)
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
def create_company(*, created_by: Profile, attrs: CompanyRevisionAttributes) -> Company:
    kwargs = attrs._asdict()
    slug = slugify(attrs.name)
    hashtags = kwargs.pop("hashtags")
    company = Company.objects.create(created_by=created_by, slug=slug)

    # Apply First Revision so we have an easy way to revert back
    revision = CompanyRevision.objects.create(
        company=company, created_by=created_by, **kwargs
    )
    revision.hashtags.set(hashtags)
    apply_revision(revision=revision, profile=created_by)

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
    revision.company.current_revision = revision
    revision.approved_by = profile
    revision.save()


def can_create_company(profile: Profile) -> bool:
    if user_is_editor(profile.user):
        return True

    pending_submissions = Company.objects.filter(
        created_by=profile, status=ModerationStatus.UNMODERATED.name
    )
    return pending_submissions.count() <= 2


def moderate_company(*, profile: Profile, company: Company, status: str) -> Company:
    company.status = status
    company.save()
    return company


def create_company_article(*, company, url, profile) -> Article:
    og_data = get_og_data(url)
    article = Article.objects.create(
        url=url, company=company, created_by=profile, opengraph_data=og_data
    )
    # Touch to udpate `_updated_at`
    company.save()
    return article


def parse_hashtag_query(query: str):
    if not query:
        return []
    return query.split(",")


def get_clapped_companies(*, profile):
    Company.clappers
