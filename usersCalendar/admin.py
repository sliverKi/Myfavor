from django.contrib import admin
from .models import UserCalendar

# 0321 수현
#pull request test
@admin.register(UserCalendar)
class UserCalendarAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "owner",
        "when"
    )
    list_display_links = (
        "id",
        "title",
        "owner",
        "when"
    )
    list_filter = ("owner","when")
    search_fields = ("=owner__nickname","when")

