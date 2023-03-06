from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from .models import User
# from django.contrib.auth import User
class TinyUserSerializers(ModelSerializer):#simple user-info
    class Meta:
        model=User
        fields=(
            "pk",
            "profileImg",
            "nickname",
            "username",
            "pick",
        )

class PrivateUserSerializer(ModelSerializer):
    class Meta:
        model=User 
        fields="__all__"