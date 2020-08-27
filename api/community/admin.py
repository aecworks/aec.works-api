from django.contrib import admin
from mptt.admin import MPTTModelAdmin

from . import models


@admin.register(models.Comment)
class CommentAdmin(MPTTModelAdmin):
    list_display = [
        "id",
        "text_start",
        "parent",
        "thread",
        "profile",
        "created_at",
        "replies",
    ]

    def text_start(self, obj):
        return f"{obj.text[:10]}..."

    def replies(self, obj):
        return obj.get_children().count()


class CommentsInline(admin.TabularInline):
    model = models.Comment


@admin.register(models.Thread)
class ThreadAdmin(admin.ModelAdmin):
    list_display = ["id", "root_comments", "thread_size"]
    inlines = [
        CommentsInline,
    ]

    def root_comments(self, obj):
        return obj.comments.count()

    def thread_size(self, obj):
        return sum(c.get_descendant_count() for c in obj.comments.all())


@admin.register(models.Company)
class CompanyAdmin(admin.ModelAdmin):
    search_fields = ("name", "description")
    list_display = [
        "id",
        "name",
        "description",
        "website",
        "twitter_handle",
        "crunchbase_id",
        "last_revision",
        "logo_url",
        "cover_url",
        "created_by",
    ]


@admin.register(models.CompanyRevision)
class CompanyRevisionAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "name",
        "description",
        "website",
        "twitter_handle",
        "crunchbase_id",
        "created_by",
        "applied",
        "approved_by",
        "logo_url",
        "cover_url",
    ]


@admin.register(models.Hashtag)
class HashtagAdmin(admin.ModelAdmin):
    list_display = ["slug"]


@admin.register(models.Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ["id", "slug", "profile", "title", "words"]

    def words(self, obj):
        return len(obj.body.split(" "))
