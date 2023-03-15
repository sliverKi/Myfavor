from django.contrib import admin
from .models import UserCalendar


@admin.register(UserCalendar)
class UserCalendarAdmin(admin.ModelAdmin):
    list_display = ("id", "title")
    list_display_links = ("id", "title")
    list_filter = ("owner",)
    search_fields = ("=owner__nickname",)
