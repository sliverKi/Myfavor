from django.db import models
from django.utils import timezone
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from common.models import CommonModel
import datetime
# from times.models import TimeModel


class Idol(models.Model):
    """Idol Model Definition"""

    class GroupChoices(models.TextChoices):
        GirlGroup = ("GirlGroup", "GirlGroup")
        BoyGroup = ("BoyGroup", "BoyGroup")

    class SoloChoices(models.TextChoices):
        GirlSolo = ("GirlSolo", "GirlSolo")
        BoySolo = ("BoySolo", "BoySolo")

    class GenderChoices(models.TextChoices):
        Woman = ("Woman", "Woman")
        Man = ("Man", "Man")

    # def group_name_validate(value):
    #     if value=="GirlGroup" or "BoyGroup":
    #         raise ValidationError("insert group name")
    #     else: return 

    Girl_group = models.CharField(
        max_length=30,
        blank=True,
        null=True,
        choices=GroupChoices.choices,
        # validators=[group_name_validate]
    )

    Boy_group = models.CharField(
        max_length=30,
        blank=True,
        null=True,
        choices=GroupChoices.choices,
    )
    idol_solo = models.CharField(
        max_length=30,
        blank=True,
        null=True,
        choices=SoloChoices.choices,
    )

    idol_name_kr = models.CharField(max_length=100, default="")
    idol_name_en = models.CharField(max_length=100, default="")
    idol_profile = models.URLField(
        max_length=10000, 
        blank=True, 
        null=True,
        #validators=[URLValidator( "유효한 URL을 입력하세요. ")]
    )

    idol_anniv = models.DateField(default=datetime.date.today)
    idol_birthday = models.DateField()

    idol_gender = models.CharField(
        max_length=5,
        choices=GenderChoices.choices,
    )

    idol_schedules = models.ManyToManyField(
        "idols.Schedule",
        blank=True,
        related_name="idols",
    )

    def str(self):
        return self.idol_name_kr

    class Meta:
        verbose_name_plural = "Our_Idols"


class Schedule(CommonModel):
    """Schedule Model Definition"""

    ScheduleTitle = models.CharField(
        max_length=150,
        default="",
    )
    ScheduleType = models.ForeignKey(
        "categories.Category",
        max_length=150,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="schedules",
    )
    location=models.CharField(
        max_length=150,
        default=""
    )
    participant = models.ManyToManyField(
        "idols.Idol",
        max_length=150,
        blank=True,
        related_name="schedules",
    )
    
    
    when=models.DateTimeField(default=timezone.now())

    class Meta:
        verbose_name_plural = "Idol-Schedules"