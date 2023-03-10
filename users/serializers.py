
from rest_framework import serializers
from .models import User
from idols.models import Idol
from datetime import date
import re
from rest_framework.exceptions import ParseError
# 신규 유저 가입 시 확인절차
class UserCreateSerializer(serializers.ModelSerializer):
    #age = serializers.SerializerMethodField()
    class Meta:
        model = User
        exclude = (
            "profileImg",
            "is_superuser",
            "first_name",
            "last_name",
            "is_staff",
            "is_active",
            "name",
            "is_admin",
            "user_permissions",
        )

    def validate_password(self, password):#비밀번호 체크 
        password_regex = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,16}$"
        if not re.match(password_regex, password):
            raise ParseError("비밀번호는 8-16자 영어 대/소문자, 숫자, 특수문자(@$!%*#?&)가 포함되어야 합니다.")
            
    def validate_age(self, age):#나이 체크  
        if age:
            if age<= 14:
                raise ParseError("15세부터 가입이 가능합니다.")
        else: raise ParseError("나이를 입력해 주세요.")    

# from django.contrib.auth import User
class TinyUserSerializers(serializers.ModelSerializer):  # simple user-info
    def get_pick(self, user, age):
        request = self.context["request"]
        return Idol.objects.filter(user=request.user, user__pk=user.pk).exists()

    class Meta:
        model = User
        fields = (
            "pk",
            "username",
            "nickname",
            "age",
            "email",
            "profileImg",
            "pick",
        )


class PrivateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = (
            "password",
            "is_superuser",
            "is_staff",
            "is_active",
            "first_name",
            "last_name",
            "groups",
            "user_permissions",
        )


class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = (
            "first_name",
            "last_name",
            "name",
        )
