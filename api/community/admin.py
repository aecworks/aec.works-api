from django.contrib import admin
from mptt.admin import MPTTModelAdmin

from .models import Company, Hashtag, Post, Comment


@admin.register(Comment)
class CommentAdmin(MPTTModelAdmin):
    list_display = ["id", "text", "parent", "profile", "created_at"]


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "name",
        "description",
        "website",
        "founded_date",
        "twitter_handle",
        "crunchbase_id",
        "employee_count",
        "logo",
        "revision_of",
        "approved_by",
        "editor",
    ]


@admin.register(Hashtag)
class HashtagAdmin(admin.ModelAdmin):
    list_display = ["name"]


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ["id", "profile", "title"]

