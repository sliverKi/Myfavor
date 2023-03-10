from rest_framework import serializers
from .models import User, NewUser
from idols.serializers import IdolsListSerializer
from idols.models import Idol
from datetime import date
import re
from rest_framework.exceptions import ParseError

# 신규 유저 가입 시 확인절차
class UserCreateSerializer(serializers.ModelSerializer):
    # password = serializers.CharField(write_only=True)

    # age = serializers.SerializerMethodField()

    # def validate_password(self, password):  # 비밀번호 체크
    #     password_regex = (
    #         r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,16}$"
    #     )
    #     if not re.match(password_regex, password):
    #         raise ParseError("비밀번호는 8-16자 영어 대/소문자, 숫자, 특수문자(@$!%*#?&)가 포함되어야 합니다.")

    # def validate_age(self, age):  # 나이 체크
    #     if age:
    #         if age <= 14:
    #             raise ParseError("15세부터 가입이 가능합니다.")
    #     else:
    #         raise ParseError("나이를 입력해 주세요.")

    class Meta:
        model = NewUser
        fields = ("username", "email", "age", "password", "pick")


class NewUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
            password = validated_data.get("password")
            user = super().create(validated_data)
            user.set_password(password)
            user.save()
            return user
    class Meta:
        model = NewUser
        field = (
            "username",
            "email",
            "password",
            "pick",
        )



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
    pick = IdolsListSerializer()

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
            "last_login",
            "name",
            "is_admin",
        )


class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = (
            "first_name",
            "last_name",
            "name",
        )
