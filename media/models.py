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
    
    # def __str__(self):
    #     return "Photo File"
    def str(self):
        return self.idol
    
class Video(CommonModel):
    title=models.CharField(max_length=150, default="")#비디오 제목
    
    VideoFile=models.URLField()

    description=models.CharField(
        max_length=150,
    )    
    def __str__(self):
        return "Video File"
