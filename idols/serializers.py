from rest_framework.serializers import ModelSerializer

from .models import Idol, Schedule

class ScheduleSerializer(ModelSerializer):
    class Meta:
        model=Schedule
        fields=("name", "description")

class IdolsListSerializer(ModelSerializer):
    class Meta:
        model=Idol
        fields=(
            "pk",
            "idol_name",
            "idol_group",
            "idol_solo",
            "idol_profile",
        )
        
        
class IdolDetailSerializer(ModelSerializer):
    
    idol_schedule=ScheduleSerializer(
        read_only=True,#스케줄을 필수 항목으로 인식하지 않음 
        many=True
    )
    class Meta:
        model=Idol
        fields="__all__"
        
