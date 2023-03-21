from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html
from .models import User, Report

# Register your models here.
@admin.register(User)
class CustomUserAdmin(UserAdmin):
    def thumbnail(self, object):
        # print(object.profileImg)
        try:
            return format_html(
                '<img src="{}" width="40" style="border-radius:50%"/>'.format(
                    object.profileImg.url,
                )
            )
        except:
            pass

    thumbnail.short_description = "profileImg"
    fieldsets = (
        (
            "Profile",
            {
                "fields": (
                    # "username",
                    "name",
                    "profileImg",
                    "nickname",
                    "email",
                    "pick",
                    "age",
                    "is_admin",
                ),
                "classes": ("wide",),
            },
        ),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
                "classes": ("collapse",),
            },
        ),
        (
            "Important dates",
            {
                "fields": ("last_login", "date_joined"),
                "classes": ("collapse",),
            },
        ),
    )

    list_display = (
        "id",
        # "username",
        "name",
        "nickname",
        "email",
        "pick",
        "is_admin",
    )
    list_display_links = (
        "email",
        "nickname",
        "name",
        # "username",
        "pick",
    )
    list_filter = ("nickname",)
    search_fields = (
        # "username",
        "name",
        "nickname",
        "name",
        "pick",
    )
    ordering = ("email",)
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("name", "email", "nickname", "password1", "password2"),
            },
        ),
    )


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "type",
        "title",
    )
    list_display_links = (
        "pk",
        "type",
        "title",
    )
