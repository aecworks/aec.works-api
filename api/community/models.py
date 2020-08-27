from django.db import models
from django_extensions.db.fields import AutoSlugField
from mptt import models as mptt_models
from django.utils.text import slugify
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver

from api.common.mixins import ReprMixin
from api.community.choices import PostBanner

from . import querysets


class CompanyBaseModel(models.Model):
    name = models.CharField(blank=False, max_length=255)
    description = models.TextField(blank=False)
    website = models.URLField(blank=False)
    location = models.CharField(max_length=64, default="")
    twitter_handle = models.CharField(max_length=15, blank=True, null=True)
    crunchbase_id = models.CharField(max_length=128, blank=True, null=True)
    logo_url = models.URLField(blank=True, null=True)
    cover_url = models.URLField(blank=True, null=True)

    class Meta:
        abstract = True


class CompanyRevision(CompanyBaseModel, ReprMixin):
    hashtags = models.ManyToManyField("Hashtag", related_name="+", blank=True)

    company = models.ForeignKey(
        "Company", on_delete=models.PROTECT, related_name="revisions",
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


class Company(CompanyBaseModel, ReprMixin):
    hashtags = models.ManyToManyField("Hashtag", related_name="companies", blank=True)

    objects = querysets.CompanyQueryset.as_manager()
    slug = AutoSlugField(populate_from="name", db_index=True)
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
    # TODO Replace with: M2M Contributors
    created_by = models.ForeignKey(
        "users.Profile", related_name="additions", on_delete=models.PROTECT,
    )
    last_revision = models.ForeignKey(
        "CompanyRevision",
        on_delete=models.PROTECT,
        related_name="+",
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name_plural = "companies"


class Hashtag(ReprMixin, models.Model):
    objects = querysets.HashtagQueryset.as_manager()
    # Note: called slug but not typical slug (removes dashes)
    # TODO: allow case?
    slug = models.SlugField(max_length=32, unique=True, db_index=True)
    # reverse: posts -> Post
    # reverse: companies -> Company


class Post(ReprMixin, models.Model):
    objects = querysets.PostQueryset.as_manager()

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
    clappers = models.ManyToManyField(
        "users.Profile", related_name="clapped_posts", blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    hot_datetime = models.DateTimeField(auto_now_add=True)
    banner = models.CharField(
        max_length=32, choices=[(c.name, c.value) for c in PostBanner], default="",
    )


class Thread(ReprMixin, models.Model):
    ...


class Comment(ReprMixin, mptt_models.MPTTModel):
    objects = querysets.CommentQueryset.as_manager()

    thread = models.ForeignKey(
        "Thread",
        related_name="comments",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
    )
    parent = mptt_models.TreeForeignKey(
        "self", on_delete=models.CASCADE, null=True, blank=True, related_name="replies"
    )
    text = models.TextField()
    profile = models.ForeignKey(
        "users.Profile", related_name="comments", on_delete=models.PROTECT
    )
    clappers = models.ManyToManyField(
        "users.Profile", related_name="clapped_comments", blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class MPTTMeta:
        order_insertion_by = ["created_at"]

    def clean(self, *args, **kwargs):
        if self.parent and self.thread:
            raise Exception("invalid parent: must a have parent or thread but not both")
        elif not self.parent and not self.thread:
            raise Exception("missing parent: comment must a have a parent or thread")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)


@receiver(post_save, sender=Company)
@receiver(post_save, sender=Post)
def add_thread(sender, instance, created, **kwargs):
    if not instance.thread:
        thread = Thread.objects.create()
        instance.thread = thread
        instance.save()


@receiver(pre_save, sender=Hashtag)
def slugify_hashtag(sender, instance, **kwargs):
    instance.slug = slugify(instance.slug).replace("-", "")


# TODO
# class ModerationFlag(ReprMixin, models.Model):
#   content_type: [ Comment | Company | Post ]
#   content: GenericForeignKey
#   flagged: [SPAN, ABUSIVE]
#   STATUS: [{PENDING, APPROVED, BLOCKED]
#   reviewer: Profile
