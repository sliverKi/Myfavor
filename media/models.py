from django.db import models
from common.models import CommonModel

class Photo(CommonModel):

    ImgFile = models.URLField()
    description = models.CharField(
        max_length=150,
    )
    idol=models.ForeignKey(
        "idols.Idol",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="photo",
    )
    user=models.ForeignKey(
        "users.User",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="photo",
    )
    def __str__(self):
        return "Photo File"
    
class Video(CommonModel):
    title=models.CharField(max_length=150, default="")
    
    VideoFile=models.URLField()

    description=models.CharField(
        max_length=150,
    )    
    def __str__(self):
        return "Video File"
