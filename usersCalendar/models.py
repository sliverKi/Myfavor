from django.db import models
from common.models import CommonModel

# 유저 캘린더
class UserCalendar(CommonModel):

    # 일정 제목
    title = models.CharField(
        max_length=50,
        blank=False,
        null=False,
    )

    # 일정 내용
    contents = models.TextField(
        max_length=500,
        default="",
        blank=True,
        null=True,
    )

    # 일정 날짜
    when = models.DateTimeField(
        auto_now=False,
        auto_now_add=False,
        blank=False,
        null=False,

    )

    # 작성자 (일정 주인 = 로그인 한 유저)
    owner = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="usercalendars",
    )
    
    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "User's Calendar"

