from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.postgres.fields import JSONField
from django.db import models
from django.db.models.signals import m2m_changed, post_delete, post_save, pre_save
from django.dispatch import receiver

from api.common.mixins import ReprMixin
from api.common.utils import to_hashtag
from api.community.choices import ModerationStatus


class CompanyRevision(ReprMixin, models.Model):
    company = models.ForeignKey(
        "Company", on_delete=models.CASCADE, related_name="revisions",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        "users.Profile", related_name="company_revisions", on_delete=models.PROTECT,
    )

    name = models.CharField(blank=False, max_length=255, db_index=True)
    description = models.TextField(blank=False)
    website = models.URLField(blank=False)
    location = models.CharField(max_length=64, default="Somewhere", db_index=True)
    twitter = models.CharField(max_length=15, blank=True, default="")
    crunchbase_id = models.CharField(max_length=128, blank=True, default="")
    logo = models.ForeignKey(
        "images.ImageAsset",
        related_name="+",
        on_delete=models.PROTECT,
        blank=True,
        null=True,
    )
    cover = models.ForeignKey(
        "images.ImageAsset",
        related_name="+",
        on_delete=models.PROTECT,
        blank=True,
        null=True,
    )
    hashtags = models.ManyToManyField("Hashtag", related_name="revisions", blank=True)
    banner = models.CharField(max_length=32, default="", blank=True)

    status = models.CharField(
        max_length=32,
        choices=[(c.name, c.value) for c in ModerationStatus],
        default=ModerationStatus.UNMODERATED.name,
    )


class Company(ReprMixin, models.Model):
    slug = models.SlugField(unique=True)
    clap_count = models.PositiveIntegerField(default=0, db_index=True)
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
    updated_at = models.DateTimeField(auto_now=True, db_index=True)
    created_by = models.ForeignKey(
        "users.Profile", related_name="additions", on_delete=models.PROTECT,
    )
    current_revision = models.OneToOneField(
        "CompanyRevision",
        on_delete=models.PROTECT,
        related_name="+",
        null=True,
        blank=False,
    )

    status = models.CharField(
        max_length=32,
        choices=[(c.name, c.value) for c in ModerationStatus],
        default=ModerationStatus.UNMODERATED.name,
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
    slug = models.CharField(max_length=32, unique=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True, db_index=True)
    # reverse: companies -> Company


class Thread(ReprMixin, models.Model):
    size = models.PositiveIntegerField(default=0)


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


class ModerationAction(ReprMixin, models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        "users.Profile", related_name="moderation_actions", on_delete=models.PROTECT,
    )

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")
    # Objects Referenced in ModerationAction must have a `status` field to store `ModerationStatus`

    status = models.CharField(
        max_length=32,
        choices=[(c.name, c.value) for c in ModerationStatus],
        default=ModerationStatus.UNMODERATED.name,
    )


class CompanyRevisionHistory(ReprMixin, models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        "users.Profile", related_name="revision_history", on_delete=models.PROTECT,
    )
    revision = models.ForeignKey(
        "CompanyRevision", on_delete=models.CASCADE, related_name="history",
    )

    class Meta:
        verbose_name_plural = "company revisions history"


@receiver(post_save, sender=Company)
def add_thread(sender, instance, created, **kwargs):
    if not instance.thread:
        thread = Thread.objects.create()
        instance.thread = thread
        instance.save()


@receiver(post_save, sender=Comment)
def increment_thread_size(sender, instance, created, **kwargs):
    if created:
        Thread.objects.filter(id=instance.thread.id).update(size=models.F("size") + 1)


@receiver(post_delete, sender=Comment)
def decrement_thread_size(sender, instance, **kwargs):
    Thread.objects.filter(id=instance.thread.id).update(size=models.F("size") - 1)


@receiver(m2m_changed, sender=Company.clappers.through)
@receiver(m2m_changed, sender=Comment.clappers.through)
def increment_company_clap(sender, instance, action, **kwargs):
    if action == "post_add":
        instance.clap_count = instance.clappers.count()
        instance.save()
    elif action == "post_remove":
        instance.clap_count = instance.clappers.count()
        instance.save()


@receiver(pre_save, sender=Hashtag)
def slugify_hashtag(sender, instance, **kwargs):
    instance.slug = to_hashtag(instance.slug)


@receiver(post_save, sender=ModerationAction)
def apply_moderation_status(sender, instance, **kwargs):
    if hasattr(instance.content_object, "status"):
        obj = instance.content_object
        obj.status = instance.status
        obj.save()
