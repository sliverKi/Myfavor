from django.db import models
from common.models import CommonModel
from idols.models import Idol

from users.models import User, Report
import datetime

# from times.models import TimeModel


class UserCalendar(CommonModel):

    title = models.CharField(
        max_length=50,
        default="",
    )  # 일정 제목

    contents = models.TextField(
        max_length=500,
        default="",
        blank=True,
        null=True,
    )  # 일정 내용

    when = models.DateTimeField(
        auto_now=False,
        auto_now_add=False,
        # default=datetime,
        blank=True,
        null=True,
    )
    owner = models.ManyToManyField(
        "users.User",
        blank=False,
    )

    pick = models.ManyToManyField(
        "idols.Idol",
        blank=False,
    )

    def __str__(self):
        return self.title

    # def __str__(self):
    #     return self.owner

    class Meta:
        verbose_name_plural = "User's Calendar"
