from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import UserCalendar
from users.models import User
from users.serializers import (
    CalendarSerializer,
    SimpleUserSerializers,
    TinyUserSerializers,
    PrivateUserSerializer,
    ReportDetailSerializer,
)

## 0322 최종 코드

from rest_framework.validators import UniqueTogetherValidator

from idols.serializers import ScheduleSerializer, IdolDetailSerializer, IdolSerializer


# 유저 일정만 있는 캘린더
class MySerializer(ModelSerializer):
    owner = CalendarSerializer(read_only=True)
    when = serializers.DateTimeField(format="%Y-%m-%d")

    class Meta:
        model = UserCalendar
        fields = (
            # "id",
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
            # "id",
            "owner",
            "title",
            "when",
            "contents",
            # "idol",
            # "idol_id",
            # "idol_schedule",
            # "idol_schedule_id",
        )


# year / month / day 로 serializer 를 각각 만든 후,
# view 에서 year, month, day 를 받아서 각각 view로 생성
# url 에서 year, month, day 를 str로 전부 받기


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
            "title",
            "contents",
        )

    def get_year(self, obj):
        return obj.when.year

    def get_month(self, obj):
        return obj.when.month

    def get_day(self, obj):
        return obj.when.day
