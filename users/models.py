from django.db import models
from django.core.validators import MinLengthValidator
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):

    name = models.CharField(
        max_length=100,
        default="",
        error_messages={"unique": "This name has already been registered."},
        # validators=[MinLengthValidator(2, "이름은 2자 이상이어야합니다.")],
    )
    nickname = models.CharField(
        max_length=100,
        default="",
        unique=True,
        # error_messages={"unique": "This nick has already been registered."},
        validators=[MinLengthValidator(3, "닉네임은 3자 이상이어야합니다.")],
    )
    email = models.EmailField(
        # null=True,
        verbose_name="Email-address",
        max_length=100,
        # unique=True,
        error_messages={"unique": "이미 사용중인 이메일입니다."},
    )
    # profileImg = models.ImageField(upload_to="profile/%Y/%m/%d", blank=True, null=True)
    profileImg = models.URLField(blank=True, null=True)
    age = models.PositiveIntegerField(default=0)
    is_admin = models.BooleanField(default=False)

    pick = models.ForeignKey(  # user는 idol을 참조
        "idols.Idol",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,  # 유저가 아이돌을 고르지 않으면 아이돌은 삭제 되면 안되지만, 유저의 선택정보를 null로 변경
        related_name="users",  # idol=user.pick
    )

    def str(self):
        return self.name

    class Meta:
        verbose_name_plural = "Our_Users"
