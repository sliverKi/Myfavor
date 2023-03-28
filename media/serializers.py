from rest_framework.serializers import ModelSerializer
from .models import Photo

class PhotoSerializer(ModelSerializer):
    class Meta:
        model=Photo
        fields=(
            "pk",
            "ImgFile",
            "description",
            "idol"
        )

class UserProfileSerializer(ModelSerializer):
    class Meta:
        model=Photo
        fields=(
            "pk",
            "ImgFile",
            "description",
            "user",
        )