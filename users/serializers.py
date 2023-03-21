import re

from rest_framework.exceptions import ParseError, ValidationError
from rest_framework import serializers

from .models import User, Report

from idols.models import Idol
from idols.serializers import IdolSerializer, IdolsListSerializer

# pick 수정용
class PickSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("pick",)


# 캘린더에서 사용할 유저 정보
class CalendarSerializer(serializers.ModelSerializer):
    pick = IdolSerializer(read_only=True)
    # is_admin = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            # "pk",
            "nickname",
            "pick",
            # "is_admin",
        )
        
    # def get_is_admin(self, user):
    #     request = self.context["request"]
    #     return user.is_admin == request.user.is_admin


# 가장 적은 유저 정보(유저 스케줄에 나타낼 정보)
class SimpleUserSerializers(serializers.ModelSerializer):
    # pick = IdolSerializer(read_only=True)
    is_admin = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            "username",
            "nickname",
            "email",
            "pick",
            "is_admin",
        )

    def get_is_admin(self, user):
        request = self.context["request"]
        return user.is_admin == request.user.is_admin


# admin 조회 용
class TinyUserSerializers(serializers.ModelSerializer):
    # pick = IdolSerializer(read_only=True)

    def get_object(self, user):
        request = self.context["request"]
        return Idol.objects.filter(user=request.user, user__pk=user.pk).exists()

    class Meta:
        model = User
        fields = (
            "pk",
            "nickname",
            "pick",
            "is_admin",
        )


# 회원가입 시 사용하는 정보
class PrivateUserSerializer(serializers.ModelSerializer):
    # pick = IdolsListSerializer(read_only=True, many=True)

    class Meta:
        model = User
        fields = (
            "name",
            "nickname",
            "pick",
            "email",
            "age",
            # "password",
        )
        
    def validate_age(self, age):
        print("check age")
        if age:
            if age <= 14 and age >= 0:
                raise ParseError("15세 부터 가입 가능합니다.")
        else:
            raise ParseError("나이를 입력해 주세요.")
        return age
    def validate_password(self, password):

        if password:
            if not re.search(r"[a-z]", password):
                raise ValidationError("비밀번호는 영문 소문자를 포함해야 합니다.")
            if not re.search(r"[A-Z]", password):
                raise ValidationError("비밀번호는 영문 대문자를 포함해야 합니다.")
            if not re.search(r"[0-9]", password):
                raise ValidationError("비밀번호는 숫자를 포함해야 합니다.")
            if not re.search(r'[~!@#$%^&*()_+{}":;\']', password):
                raise ValidationError("비밀번호는 특수문자(~!@#$%^&*()_+{}\":;')를 포함해야 합니다.")
            if len(password) < 8 or len(password) > 16:
                raise ValidationError("비밀번호는 8자 이상 16자 이하이어야 합니다.")
            print(password)
        else:
            raise ParseError("비밀번호를 입력하세요.")
        return password
    

# admin이 유저 정보를 조회할 때 사용하는 정보
class UserSerializer(serializers.ModelSerializer):

    pick = IdolSerializer(read_only=True)
    is_admin = serializers.SerializerMethodField()

    class Meta:
        model = User

        fields = (
            "id",
            "username",
            "nickname",
            "age",
            "email",
            "pick",
            "is_admin",
            # "date_joined",
            # "is_superuser",
            # "is_staff",
        )

    def get_is_admin(self, user):
        request = self.context["request"]
        return user.is_admin == request.user.is_admin


class ReportDetailSerializer(serializers.ModelSerializer):
    owner = TinyUserSerializers(read_only=True)
    whoes = IdolSerializer(many=True, read_only=True)

    class Meta:
        model = Report
        fields = "__all__"
