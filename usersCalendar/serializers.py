from rest_framework.serializers import ModelSerializer
from .models import UserCalendar
from users.models import User
from users.serializers import (
    TinyUserSerializers,
    PrivateUserSerializer,
    ReportDetailSerializer,
)

from idols.serializers import ScheduleSerializer, IdolDetailSerializer


class UserCalendarSerializer(ModelSerializer):
    pick = IdolDetailSerializer([])

    class Meta:
        model = UserCalendar
        fields = [
            "id",
            "owner",
            "title",
            "contents",
            "pick",
        ]

    owner = PrivateUserSerializer("get_nickname")

    def get_nickname(self, obj):
        return obj.owner


class UserDetailSerializer(ModelSerializer):
    class Meta:
        model = UserCalendar
        fields = [
            "id",
            "nickname",
            "title",
            "contents",
            "when",
            "pick",
            # "pick_schedule",
        ]


class MyScheduleSerializer(ModelSerializer):
    class Meta:
        model = UserCalendar
        fields = [
            "pk",
            "title",
            "contents",
            "when",
        ]

    # pick = ScheduleSerializer("get_idol_schedule")

    # def get_idol_schedule(self,obj):
    # return obj.idol.schedule


# class UserCalendarSerializer(ModelSerializer):
#     owner = TinyUserSerializers([])

#     class Meta:
#         model = UserCalendar
#         exclude = (
#             "updated_at",
#             "created_at",
#         )


# class UserDetailSerializer(ModelSerializer):
#     owner = UserOwnerSerializer([])
#     # owner = UserOwnerSerializer(many=True)

#     class Meta:
#         model = UserCalendar
#         fields = [
#             "owner",
#             "title",
#             "when",
#             "contents",
#         ]
