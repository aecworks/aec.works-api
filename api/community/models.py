from django.db import models
from django.contrib.postgres.fields import JSONField
from django_extensions.db.fields import AutoSlugField
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver

from api.common.utils import to_hashtag
from api.common.mixins import ReprMixin
from api.community.choices import PostBanner

from . import querysets


class CompanyBaseModel(models.Model):
    name = models.CharField(blank=False, max_length=255)
    description = models.TextField(blank=False)
    website = models.URLField(blank=False)
    location = models.CharField(max_length=64, default="")
    twitter = models.CharField(max_length=15, blank=True, null=True)
    crunchbase_id = models.CharField(max_length=128, blank=True, null=True)
    logo = models.ForeignKey(
        "images.ImageAsset",
        related_name="+",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    cover = models.ForeignKey(
        "images.ImageAsset",
        related_name="+",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )

    class Meta:
        abstract = True


class CompanyRevision(ReprMixin, CompanyBaseModel):
    # TODO: Rethink Revision model -
    # to diff based eg. Revision.diffs = [{"field": "name", op: "delete"}]
    hashtags = models.ManyToManyField("Hashtag", related_name="+", blank=True)

    company = models.ForeignKey(
        "Company", on_delete=models.CASCADE, related_name="revisions",
    )
    applied = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    approved_by = models.ForeignKey(
        "users.Profile",
        related_name="company_approvals",
        on_delete=models.PROTECT,
        null=True,
    )
    created_by = models.ForeignKey(
        "users.Profile", related_name="company_revisions", on_delete=models.PROTECT,
    )


class Company(ReprMixin, CompanyBaseModel):
    hashtags = models.ManyToManyField("Hashtag", related_name="companies", blank=True)

    slug = AutoSlugField(populate_from="name", db_index=True)
    clap_count = models.PositiveIntegerField(default=0)
    clappers = models.ManyToManyField(
        "users.Profile", related_name="clapped_companies", blank=True
    )
    thread = models.OneToOneField(
        "Thread",
        related_name="post",
        unique=True,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        "users.Profile", related_name="additions", on_delete=models.PROTECT,
    )
    last_revision = models.ForeignKey(
        "CompanyRevision",
        on_delete=models.SET_NULL,
        related_name="+",
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name_plural = "companies"
        permissions = [("apply_companyrevision", "Can Apply Revision")]


class Article(ReprMixin, models.Model):
    url = models.URLField()
    company = models.ForeignKey(
        "Company", on_delete=models.CASCADE, related_name="articles"
    )
    opengraph_data = JSONField(default=dict, blank=True)
    created_by = models.ForeignKey(
        "users.Profile", related_name="articles", on_delete=models.PROTECT,
    )


class Hashtag(ReprMixin, models.Model):
    objects = querysets.HashtagQueryset.as_manager()
    slug = models.CharField(max_length=32, unique=True, db_index=True)
    # reverse: posts -> Post
    # reverse: companies -> Company


class Post(ReprMixin, models.Model):

    title = models.CharField(blank=False, max_length=100)
    slug = AutoSlugField(populate_from="title", db_index=True)

    body = models.TextField(blank=False)
    profile = models.ForeignKey(
        "users.Profile", related_name="posts", on_delete=models.PROTECT
    )
    thread = models.ForeignKey(
        "Thread", related_name="+", on_delete=models.CASCADE, blank=True, null=True
    )
    companies = models.ManyToManyField(Company, related_name="posts", blank=True)
    hashtags = models.ManyToManyField(Hashtag, related_name="posts", blank=True)
    clap_count = models.PositiveIntegerField(default=0)
    clappers = models.ManyToManyField(
        "users.Profile", related_name="clapped_posts", blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    hot_datetime = models.DateTimeField(auto_now_add=True)
    banner = models.CharField(
        max_length=32, choices=[(c.name, c.value) for c in PostBanner], default="",
    )
    cover = models.ForeignKey(
        "images.ImageAsset",
        related_name="post_covers",
        on_delete=models.PROTECT,
        blank=True,
        null=True,
    )
    images = models.ManyToManyField("images.ImageAsset", related_name="posts")


class Thread(ReprMixin, models.Model):
    ...


class Comment(ReprMixin, models.Model):

    thread = models.ForeignKey(
        "Thread", related_name="comments", on_delete=models.CASCADE,
    )
    text = models.TextField()
    profile = models.ForeignKey(
        "users.Profile", related_name="comments", on_delete=models.PROTECT
    )
    clap_count = models.PositiveIntegerField(default=0)
    clappers = models.ManyToManyField(
        "users.Profile", related_name="clapped_comments", blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at"]


@receiver(post_save, sender=Company)
@receiver(post_save, sender=Post)
def add_thread(sender, instance, created, **kwargs):
    if not instance.thread:
        thread = Thread.objects.create()
        instance.thread = thread
        instance.save()


@receiver(pre_save, sender=Hashtag)
def slugify_hashtag(sender, instance, **kwargs):
    instance.slug = to_hashtag(instance.slug)


# TODO
# class ModerationFlag(ReprMixin, models.Model):
#   content_type: [ Comment | Company | Post ]
#   content: GenericForeignKey
#   flagged: [SPAN, ABUSIVE]
#   STATUS: [{PENDING, APPROVED, BLOCKED]
#   reviewer: Profile
