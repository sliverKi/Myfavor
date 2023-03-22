from django.db import models
from django.core.validators import MinLengthValidator, MinValueValidator
from django.contrib.auth.models import (
    AbstractUser,
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.utils import timezone
from categories.models import Category
from datetime import datetime
from .manager import CustomUserManager

# user
class User(AbstractUser):
    username = None  # username을 사용 안할 경우
    name = models.CharField(
        # 동명이인 생각하기
        max_length=100,
        # default="",
        blank=False,
        validators=[MinLengthValidator(2, "이름은 2자 이상이어야합니다.")],
    )
    nickname = models.CharField(
        max_length=100,
        unique=True,
        blank=False,
        validators=[MinLengthValidator(3, "닉네임은 3자 이상이어야합니다.")],
    )
    email = models.EmailField(
        blank=False,
        verbose_name="Email-address",
        max_length=100,
        unique=True,
        error_messages={"unique": "이미 사용중인 이메일입니다."},
    )
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    profileImg = models.URLField(blank=True, null=True, default="https://audition.hanbiton.com/images/common/img_default.jpg")

    age = models.PositiveIntegerField(
        blank=False,
        default=0,
        validators=[
            MinValueValidator(15, "15세 이상부터 가입이 가능합니다."),
        ],
    )

    is_admin = models.BooleanField(default=False)  # 관리자 - 사용자 구분

    pick = models.ForeignKey(
        "idols.Idol",
        # default="",
        blank=False,
        null=True,
        on_delete=models.SET_NULL,
        related_name="users",
    )
    reports = models.ManyToManyField(
        "users.Report",
        null=True,
        blank=True,
        related_name="users",
    )

    def str(self):
        return self.name

    class Meta:
        verbose_name_plural = "Our_Users"


# 제보
class Report(Category):

    owner = models.ForeignKey(  # 작성자
        "users.User",
        max_length=100,
        default="",
        on_delete=models.CASCADE,
        related_name="report",
    )

    title = models.CharField(max_length=100, default="")
    location = models.CharField(max_length=100, default="")
    time = models.DateTimeField(default=datetime.now)
    whoes = models.ManyToManyField(  # 참여자 (paticipant)
        "idols.Idol",
        null=True,
        blank=True,
        related_name="report",
    )



    def str(self):
        return self.title

    class Meta:
        verbose_name_plural = "User Report"
