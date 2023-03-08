# from rest_framework import serializers
from rest_framework import serializers
from .models import User
from idols.models import Idol
from datetime import date
#copy
# from django.contrib.auth import User
class TinyUserSerializers(serializers.ModelSerializer):  # simple user-info
    def get_pick(self, user):
        request = self.context["request"]
        return Idol.objects.filter(user=request.user, user__pk=user.pk).exists()

    class Meta:
        model = User
        fields = (
            "pk",
            "username",
            "nickname",
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


# 신규 유저 가입 시 확인절차
# class UserCreateSerializer(serializers.ModelSerializer):
#     age = serializers.SerializerMethodField()

#     # 15세 미만이면 false
#     def get_event_age(self, age):
#         return True if age > 15 else False

#     class Meta:
#         model = User
#         fields = "__all__"

#     def validate_age(self, age):
#         if age < 15:
#             raise serializers.ValidationError("나이는 15 이상이어야 합니다.")
#         return age

#     def validate_name(self, name):
#         if len(name) <= 2:
#             raise serializers.ValidationError("이름은 2자 이상이어야 합니다.")

#     # 이메일 유효성 검사 // 임데 admin..?
#     def validate_email(self, email):
#         if "admin" in email:
#             raise serializers.ValidationError("사용할 수 없는 이메일입니다.")
#         return email
