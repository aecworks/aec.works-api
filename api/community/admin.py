from django.contrib import admin
from mptt.admin import MPTTModelAdmin

from api.common.utils import get_og_data
from . import models


@admin.register(models.Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ["id", "url", "company", "created_by"]

    def save_model(self, request, obj, form, change):
        og_data = get_og_data(obj.url)
        obj.opengraph_data = og_data
        obj.save()
        super().save_model(request, obj, form, change)


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
    list_display = ["id", "root_comments", "size"]
    inlines = [
        CommentsInline,
    ]

    def root_comments(self, obj):
        return obj.comments.count()


@admin.register(models.Company)
class CompanyAdmin(admin.ModelAdmin):
    search_fields = ("name", "description")
    list_display = [
        "id",
        "name",
        "descrition_start",
        "website",
        "twitter",
        "crunchbase_id",
        "last_revision",
        "logo",
        "cover",
        "created_by",
    ]
    raw_id_fields = ["logo", "cover"]
    readonly_fields = ["thread"]

    def descrition_start(self, obj):
        return f"{obj.description[:10]}..."


@admin.register(models.CompanyRevision)
class CompanyRevisionAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "name",
        "description",
        "website",
        "twitter",
        "crunchbase_id",
        "created_by",
        "applied",
        "approved_by",
        "logo",
        "cover",
    ]
    raw_id_fields = ["logo", "cover"]


@admin.register(models.Hashtag)
class HashtagAdmin(admin.ModelAdmin):
    list_display = ["slug", "post_count", "company_names"]

    def company_names(self, obj):
        return [c.name for c in obj.companies.all()]

    def post_count(self, obj):
        return obj.posts.count()


@admin.register(models.Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ["id", "slug", "profile", "title", "cover", "words"]

    def words(self, obj):
        return len(obj.body.split(" "))

    raw_id_fields = ["cover"]
