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

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        qs = qs.prefetch_related("comments")
        return qs


@admin.register(models.Company)
class CompanyAdmin(admin.ModelAdmin):
    search_fields = ("name", "description")
    list_display = [
        "id",
        admin_related("current_revision", "name"),
        "descrition_start",
        "status",
        admin_related("current_revision", "website"),
        admin_related("current_revision", "twitter"),
        admin_related("current_revision", "crunchbase_id"),
        admin_related("current_revision", "logo"),
        admin_related("current_revision", "cover"),
        admin_linkify(field_name="thread"),
        admin_linkify(field_name="current_revision"),
        admin_linkify(field_name="created_by"),
    ]

    readonly_fields = ["thread"]

    def descrition_start(self, obj):
        return f"{obj.current_revision.description[:10]}..."

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        qs = qs.select_related(
            "thread",
            "created_by__user",
            "current_revision__logo",
            "current_revision__cover",
            "current_revision__created_by__avatar",
            "current_revision__created_by__user",
        ).prefetch_related("current_revision__hashtags", "articles")
        return qs


@admin.register(models.CompanyRevision)
class CompanyRevisionAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "name",
        "status",
        "description",
        "website",
        "twitter",
        "crunchbase_id",
        "created_by",
        "logo",
        "cover",
    ]
    raw_id_fields = ["logo", "cover"]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        qs = qs.select_related("created_by__user", "logo", "cover")
        return qs


class CompanyRevisionInline(admin.TabularInline):
    model = models.CompanyRevision.hashtags.through


@admin.register(models.Hashtag)
class HashtagAdmin(admin.ModelAdmin):
    list_filter = ["revisions__company"]
    list_display = ["slug", "company_names"]
    inlines = [
        CompanyRevisionInline,
    ]

    def company_names(self, obj):
        return ", ".join(set([c.name for c in obj.revisions.all()]))

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        qs = qs.prefetch_related("revisions")
        return qs


@admin.register(models.ModerationAction)
class ModerationActionAdmin(admin.ModelAdmin):
    list_filter = ("content_object", "created_by", "status")
    list_display = [
        "id",
        "content_type",
        admin_linkify("content_object"),
        "status",
        admin_linkify("created_by"),
    ]

    readonly_fields = ["content_type", "content_object", "status", "created_by"]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        qs = qs.select_related("created_by__user").prefetch_related("content_object")
        return qs


@admin.register(models.CompanyRevisionHistory)
class CompanyRevisionHistoryAdmin(admin.ModelAdmin):
    list_filter = ("created_by", "revision__company")
    list_display = [
        "id",
        "created_at",
        admin_linkify("created_by"),
        admin_linkify("revision"),
        admin_linkify("revision.company"),
    ]

    readonly_fields = ["created_by", "revision", "created_at"]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        qs = qs.select_related("created_by__user", "revision__company")
        return qs
