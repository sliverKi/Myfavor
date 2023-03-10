from rest_framework.serializers import ModelSerializer
from .models import UserCalendar


class UserCalendarSerializer(ModelSerializer):
    owner = UserCalendar()

    class Meta:
        model = UserCalendar
        fields = (
            "pk",
            "owner",  # username = 일정주인
            "title",
            "content",
            # "start_date",
            # "end_date",
        )


# class UserDetailsSerializer(ModelSerializer):
