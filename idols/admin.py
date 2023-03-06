from django.contrib import admin
from .models import Idol, Schedule
@admin.register(Idol)
class Idols(admin.ModelAdmin):
    list_display = ("id","idol_name", "idol_group","idol_solo")
    list_display_links=("id", "idol_name",)
    search_fields=("idol_name",)

@admin.register(Schedule)
class AScheduleAdmin(admin.ModelAdmin):
    list_display = (
        
        "name",
        "description",
        "created_at",
        "updated_at",
        
    )
    readonly_fields = (
        "created_at",
        "updated_at",
    )
