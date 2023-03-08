from django.utils import timezone
from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import Idol, Schedule
from categories.serializers import CategorySerializer
class IdolsListSerializer(ModelSerializer):
    class Meta:
        model = Idol
        fields = ("pk", "idol_name", "idol_group","idol_solo", "idol_profile", )

class ScheduleSerializer(ModelSerializer):
    ScheduleType = CategorySerializer()
    participant = IdolsListSerializer(many=True, read_only=True)
    
    when=serializers.DateTimeField()

    class Meta:
        model = Schedule
        fields = (
            "pk",
            "ScheduleTitle",
            "ScheduleType",
            "location",
            "when",
            "description",
            "participant",
        )
    


class IdolDetailSerializer(ModelSerializer):

    idol_schedules = ScheduleSerializer(
        read_only=True, many=True  # 스케줄을 필수 항목으로 인식하지 않음
    )

    class Meta:
        model = Idol
        fields = "__all__"
