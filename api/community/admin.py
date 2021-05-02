from django.contrib import admin

from api.common.utils import admin_linkify, admin_related, get_og_data

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
class CommentAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "text_start",
        "thread",
        "profile",
        "created_at",
    ]

    def text_start(self, obj):
        return f"{obj.text[:10]}..."


class CommentsInline(admin.TabularInline):
    model = models.Comment


@admin.register(models.Thread)
class ThreadAdmin(admin.ModelAdmin):
    list_display = ["id", "comment_count"]
    inlines = [
        CommentsInline,
    ]

    def comment_count(self, obj):
        return obj.comments.count()


@admin.register(models.Company)
class CompanyAdmin(admin.ModelAdmin):
    search_fields = ("name", "description")
    list_display = [
        "id",
        admin_related("current_revision", "name"),
        admin_related("current_revision", "name"),
        admin_related("current_revision", "website"),
        admin_related("current_revision", "twitter"),
        admin_related("current_revision", "crunchbase_id"),
        "descrition_start",
        admin_related("current_revision", "logo"),
        admin_related("current_revision", "cover"),
        # admin_linkify(field_name="logo"),
        # admin_linkify(field_name="cover"),
        admin_linkify(field_name="thread"),
        admin_linkify(field_name="current_revision"),
        admin_linkify(field_name="created_by"),
    ]
    # raw_id_fields = ["logo", "cover"]
    readonly_fields = ["thread"]

    def descrition_start(self, obj):
        return f"{obj.current_revision.description[:10]}..."


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
        "logo",
        "cover",
    ]
    raw_id_fields = ["logo", "cover"]


@admin.register(models.Hashtag)
class HashtagAdmin(admin.ModelAdmin):
    list_display = ["slug", "company_names"]

    def company_names(self, obj):
        return [c.name for c in obj.companies.all()]
