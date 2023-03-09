# from rest_framework import serializers
from rest_framework import serializers
from .models import User
from idols.models import Idol
from datetime import date


# 신규 유저 가입 시 확인절차
class UserCreateSerializer(serializers.ModelSerializer):
    #     # age = serializers.SerializerMethodField()

    #     # # 15세 미만이면 false
    #     # def age(self, age):
    #     #     return True if age >= 15 else False

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


#     def validate_age(self, age):
#         if age <= 15:
#             raise serializers.ValidationError("나이는 15세 이상이어야 합니다.")
#         return age

#     def validate_name(self, name):
#         if len(name) <= 2:
#             raise serializers.ValidationError("이름은 2자 이상이어야 합니다.")
#         return name

#     # 이메일 유효성 검사 // 임데 admin..?
#     def validate_email(self, email):
#         if "admin" in email:
#             raise serializers.ValidationError("사용할 수 없는 이메일입니다.")
#         return email


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
