from django.db import models
from accounts.models import CustomUserManager
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


class CustomAbstractUser(AbstractUser):
    # username = None  # username을 사용 안할 경우
    email = models.EmailField(("email address"), unique=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email
