from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import UserCalendar
from users.models import User
from users.serializers import (
    CalendarSerializer,
    SimpleUserSerializers,

)

## 0322 최종 코드


# 유저 일정만 있는 캘린더
class MySerializer(ModelSerializer):
    owner = CalendarSerializer(read_only=True)
    when = serializers.DateTimeField(format="%Y-%m-%d")

    class Meta:
        model = UserCalendar
        fields = (
            "pk",
            "owner",
            "title",
            "when",
            "contents",
        )


class MyDetailSerializer(ModelSerializer):
    owner = SimpleUserSerializers(read_only=True)
    when = serializers.DateTimeField(format="%Y-%m-%d")

    class Meta:
        model = UserCalendar
        fields = (
            "pk",
            "owner",
            "title",
            "when",
            "contents",
            # "idol",
            # "idol_id",
            # "idol_schedule",
            # "idol_schedule_id",
        )



class DateSerializer(ModelSerializer):
    owner = CalendarSerializer(read_only=True)

    year = serializers.SerializerMethodField()
    month = serializers.SerializerMethodField()
    day = serializers.SerializerMethodField()

    class Meta:
        model = UserCalendar
        fields = (
            "owner",
            "year",
            "month",
            "day",
            "pk",
            "title",
            "contents",
        )

    def get_year(self, obj):
        return obj.when.year

    def get_month(self, obj):
        return obj.when.month

    def get_day(self, obj):
        return obj.when.day


