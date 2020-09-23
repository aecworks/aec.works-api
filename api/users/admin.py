from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

from .models import User, Profile


class CustomBaseUserAdmin(BaseUserAdmin):
    # Because we overided the UserModel, we need to modify UserAdmin to exlude fields
    ordering = ["email"]
    list_display = ["email", "is_staff"]
    fieldsets = (
        (None, {"fields": ("email", "password")}),
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
        (None, {"classes": ("wide",), "fields": ("email", "password1", "password2")},),
    )
    search_fields = ("email", "name")


# Register your models here.
@admin.register(User)
class UserAdmin(CustomBaseUserAdmin):
    ...


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ["user", "twitter", "location", "name"]
