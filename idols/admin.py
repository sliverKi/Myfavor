from django.contrib import admin
from .models import Idol, Schedule

# from times.models import TimeModel


@admin.register(Idol)
class Idols(admin.ModelAdmin):
    list_display = ("id", "idol_name_kr","idol_name_en","Girl_group","Boy_group", "idol_solo")
    list_display_links = (
        "id",
        "idol_name_kr",
        "idol_name_en"
    )
    search_fields = (
        "idol_name_kr",
        "idol_name_en",
        "Girl_group",
        "Boy_group",
        #"idol_group",
    )


@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "ScheduleTitle",
        "ScheduleType",
        "when",
        "created_at",
        "updated_at",
    )
    list_display_links = (
        "pk",
        "ScheduleTitle",
        "ScheduleType"
    
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )