from django.db import models
from django.core.validators import MinLengthValidator, MinValueValidator
from django.contrib.auth.models import (
    AbstractUser,
)

from categories.models import Category
from datetime import datetime
from .manager import CustomUserManager

# user
class User(AbstractUser):
    username = None  
    name = models.CharField(
        max_length=100,
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

    profileImg = models.URLField(
        blank=True, 
        null=True, 
        default="https://api.cloudflare.com/client/v4/accounts/135e63e511ff302b43eaab2356b50bf6/images/v1/fccba4a0-df32-485d-8c6f-9410b97c2100"
    )

    age = models.PositiveIntegerField(
        blank=False,
        default=0,
        validators=[
            MinValueValidator(15, "15세 이상부터 가입이 가능합니다."),
        ],
    )

    is_admin = models.BooleanField(default=False)  

    pick = models.ForeignKey(
        "idols.Idol",
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

    owner = models.ForeignKey(  
        "users.User",
        max_length=100,
        default="",
        on_delete=models.CASCADE,
        related_name="report",
    )

    title = models.CharField(max_length=100, default="")
    location = models.CharField(max_length=100, default="")
    time = models.DateTimeField(default=datetime.now)
    whoes = models.ManyToManyField(  
        "idols.Idol",
        null=True,
        blank=True,
        related_name="report",
    )



    def str(self):
        return self.title

    class Meta:
        verbose_name_plural = "User Report"
