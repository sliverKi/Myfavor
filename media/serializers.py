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

        # {  
            # "ImgFile":"https://i.ytimg.com/vi/pz_1O1GA43c/maxresdefault.jpg",
            # "description":"JISU",
            # "idol":1,
        # }