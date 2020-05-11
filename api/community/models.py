from django.db import models
from mptt import models as mptt_models

from api.common.utils import to_slug
from api.common.mixins import ReprMixin
from .choices import EmployeeCountChoices


class Company(ReprMixin, models.Model):
    name = models.CharField(blank=False, max_length=255)
    slug = models.CharField(
        blank=True, null=False, max_length=255, unique=True, db_index=True
    )
    description = models.TextField(blank=False)
    website = models.URLField(blank=False)

    # Optional
    founded_date = models.DateField(blank=True, null=True)
    twitter_handle = models.CharField(max_length=15, blank=True, null=True)
    crunchbase_id = models.CharField(max_length=128, blank=True, null=True)
    employee_count = models.CharField(
        blank=True,
        null=True,
        max_length=32,
        choices=[(c.name, c.value) for c in EmployeeCountChoices],
        default=EmployeeCountChoices.TEN.name,
    )
    logo = models.ImageField(upload_to="logos", null=True, blank=True)
    hashtags = models.ManyToManyField("Hashtag", related_name="companies", blank=True)
    clappers = models.ManyToManyField(
        "users.Profile", related_name="clapped_companies", blank=True
    )
    root_comment = models.ForeignKey(
        "Comment", related_name="+", on_delete=models.SET_NULL, blank=True, null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)

    revision_of = models.ForeignKey(
        "Company",
        related_name="revisions",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    replaced_by = models.ForeignKey(
        "Company",
        related_name="replaced",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    approved_by = models.ForeignKey(
        "users.Profile",
        related_name="approvals",
        on_delete=models.PROTECT,
        blank=True,
        null=True,
    )
    editor = models.ForeignKey(
        "users.Profile",
        related_name="revisions",
        on_delete=models.PROTECT,
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name_plural = "companies"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = to_slug(self.name)
        super().save(*args, **kwargs)


class Hashtag(ReprMixin, models.Model):
    name = models.CharField(max_length=32, unique=True, db_index=True)
    # posts -> Post
    # companies -> Company


class Post(ReprMixin, models.Model):

    title = models.CharField(blank=False, max_length=100)
    slug = models.CharField(
        blank=True, null=False, max_length=100, unique=True, db_index=True
    )

    body = models.TextField(blank=False)
    profile = models.ForeignKey(
        "users.Profile", related_name="posts", on_delete=models.PROTECT
    )
    root_comment = models.ForeignKey(
        "Comment", related_name="+", on_delete=models.SET_NULL, blank=True, null=True
    )
    companies = models.ManyToManyField(Company, related_name="posts", blank=True)
    hashtags = models.ManyToManyField(Hashtag, related_name="posts", blank=True)
    clappers = models.ManyToManyField(
        "users.Profile", related_name="clapped_posts", blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = to_slug(self.title)
        super().save(*args, **kwargs)


class Comment(ReprMixin, mptt_models.MPTTModel):
    text = models.TextField()
    parent = mptt_models.TreeForeignKey(
        "self", on_delete=models.CASCADE, null=True, blank=True, related_name="replies"
    )
    profile = models.ForeignKey(
        "users.Profile", related_name="comments", on_delete=models.PROTECT
    )
    clappers = models.ManyToManyField(
        "users.Profile", related_name="clapped_comments", blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class MPTTMeta:
        order_insertion_by = ["created_at"]


# class ModerationFlag(ReprMixin, models.Model):
#   content_type: [ Comment | Company | Post ]
#   content: GenericForeignKey
#   flagged: [SPAN, ABUSIVE]
#   STATUS: [{PENDING, APPROVED, BLOCKED]
#   reviewer: Profile
