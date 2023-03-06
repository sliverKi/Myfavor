from django.contrib import admin
from .models import Idol, Schedule

# from times.models import TimeModel


@admin.register(Idol)
class Idols(admin.ModelAdmin):
    list_display = ("id", "idol_name", "idol_group", "idol_solo")
    list_display_links = (
        "id",
        "idol_group",
        "idol_name",
    )
    search_fields = (
        "idol_name",
        "idol_group",
    )


@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = (
        "ScheduleTitle",
        # "start_time",
        # "description",
        "created_at",
        "updated_at",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )
