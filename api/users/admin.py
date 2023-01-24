from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

from api.common.utils import admin_linkify

from .models import Profile, User


class CustomBaseUserAdmin(BaseUserAdmin):
    # Because we overided the UserModel, we need to modify UserAdmin to exlude fields
    ordering = ["email"]
    list_display = [
        "name",
        "email",
        "get_provider_display",
        "is_editor",
        "is_staff",
        admin_linkify("profile"),
    ]
    fieldsets = (
        (None, {"fields": ("email", "password", "provider")}),
        (_("Personal info"), {"fields": ("name",)}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            None,
            {"classes": ("wide",), "fields": ("email", "password1", "password2")},
        ),
    )
    search_fields = ("email", "name")

    def is_editor(self, obj) -> bool:
        return "editors" in [g.name for g in obj.groups.all()]

    is_editor.boolean = True
    is_editor.admin_order_field = "groups__name"


# Register your models here.
@admin.register(User)
class UserAdmin(CustomBaseUserAdmin):
    search_fields = ("name", "email")

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        qs = qs.select_related("profile__avatar").prefetch_related("groups")
        return qs


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        admin_linkify("user"),
        "slug",
        "twitter",
        "location",
        "name",
        "github",
        admin_linkify("avatar"),
    ]
    search_fields = ["user__name"]
    raw_id_fields = ["avatar"]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        qs = qs.select_related("avatar", "user")
        return qs
