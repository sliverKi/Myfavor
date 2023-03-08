from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):

    name = models.CharField(max_length=100, default="")
    nickname = models.CharField(max_length=100, default="", unique=True)
    email = models.EmailField(
        verbose_name="Email-address",
        max_length=100,
        unique=True,
    )
    profileImg = models.ImageField(upload_to="profile/%Y/%m/%d", blank=True, null=True)
    age = models.PositiveIntegerField(default=0)
    is_admin = models.BooleanField(default=False)

    pick = models.ForeignKey(  # user는 idol을 참조
        "idols.Idol",
        null=True,
        on_delete=models.SET_NULL,  # 유저가 아이돌을 고르지 않으면 아이돌은 삭제 되면 안되지만, 유저의 선택정보를 null로 변경
        related_name="users",  # idol=user.pick
    )

    def str(self):
        return self.name

    class Meta:
        verbose_name_plural = "Our_Users"
