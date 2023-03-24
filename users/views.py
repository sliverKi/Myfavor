from datetime import timedelta
from django.utils import timezone
from django.urls import reverse_lazy
from rest_framework.generics import GenericAPIView
from django.contrib.auth.tokens import PasswordResetTokenGenerator

from django.http import HttpResponse, JsonResponse, HttpResponseRedirect


from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView

from tokenize import generate_tokens
from django.shortcuts import render, redirect
from django.db import transaction
from django.contrib.auth import login, logout
from django.urls import reverse

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_403_FORBIDDEN,
    HTTP_302_FOUND,
)

from rest_framework.exceptions import (
    NotFound,
    ParseError,
    PermissionDenied,
    NotAuthenticated,
)
from django.core.exceptions import ValidationError
from rest_framework.permissions import (
    IsAuthenticated,
    IsAuthenticatedOrReadOnly,
    IsAdminUser,
)

from .models import User, Report
from .serializers import (
    TinyUserSerializers,
    PrivateUserSerializer,
    ReportDetailSerializer,
    SimpleUserSerializers,
    UserSerializer,
    PickSerializer,
    FindPasswordSerializer,HtmlSerializer,
)

from django.conf import settings


from idols.serializers import IdolSerializer
from idols.models import Idol

from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import send_mail

from .token import account_activation_token


# 신규 유저 추가  :: OK
# "age", "pick", "email", "password"
class NewUsers(APIView):
    def get(self, request):
        return Response({"email, password, nickname, age, pick 을 입력해주세요."})

    def post(self, request):

        password = request.data.get("password")

        if not password:
            raise ParseError
        serializer = PrivateUserSerializer(data=request.data)
        print(password)

        if serializer.is_valid():
            user = serializer.save()
            user.set_password(password)
            user.save()
            serializer = PrivateUserSerializer(user)
            return Response(serializer.data, status=HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


# 모든 유저 조회 / userlist
## admin 용  :: OK
class AllUsers(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):  # 조회
        all_users = User.objects.all()  # 모든 Users 불러와
        serializer = UserSerializer(
            all_users,
            many=True,
            context={"request": request},
        )
        return Response(serializer.data, status=HTTP_200_OK)


# 유저 정보 조회 및 수정 및 삭제  :: OK
## url로 들어가면 유저 본인 페이지만 나옴 (로그인 필요)
### user용
class MyPage(APIView):  # OK
    permission_classes = [IsAuthenticated]

    # 유저 정보 조회
    def get(self, request):
        user = request.user
        serializer = TinyUserSerializers(user)
        return Response(serializer.data)

    # 유저 정보 update
    def put(self, request):
        user = request.user
        serializer = TinyUserSerializers(
            user,
            data=request.data,
            partial=True,
        )
        if serializer.is_valid():
            user = serializer.save()
            serializer = TinyUserSerializers(user)
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

    def delete(self, request):
        user = request.user
        user.delete()
        return Response({"message": "계정이 삭제되었습니다."}, status=HTTP_204_NO_CONTENT)


# pk로 조회 (수정 및 삭제 가능)
## admin 조회용 (모든 정보 나타내기)  :: OK
class UserDetail(APIView):  # OK
    permission_classes = [IsAdminUser]  # admin만 열람 가능

    # 유저 정보 조회
    def get(self, request, pk):
        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise NotFound()
        serializer = PrivateUserSerializer(user)
        return Response(serializer.data, status=HTTP_200_OK)

    # 유저 정보 수정
    def put(self, request, pk):
        user = User.objects.get(pk=pk)
        serializer = TinyUserSerializers(
            user,
            data=request.data,
            partial=True,
        )
        if serializer.is_valid():
            user = serializer.save()
            serializer = TinyUserSerializers(user)
            return Response(serializer.data, status=HTTP_200_OK)
        else:
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

    # 유저 삭제
    def delete(self, request, pk):
        user = User.objects.get(pk=pk)
        user.delete()
        return Response({"message": "계정이 삭제되었습니다."}, status=HTTP_204_NO_CONTENT)


# 유저 비번 변경 -> OK
## (본인만 열람 가능) / url로 들어가면 본인계정으로만 들어가게 됨
### user 용
class EditPassword(APIView):  # OK
    permission_classes = [IsAuthenticated]

    def put(self, request):
        user = request.user
        old_password = request.data.get("old_password")
        new_password = request.data.get("new_password")

        if not old_password or not new_password:
            raise ParseError

        if user.check_password(old_password):
            if old_password != new_password:
                user.set_password(new_password)
                user.save()
                return Response({"비밀번호가 성공적으로 변경되었습니다."})
            else:
                return Response({"변경 될 비밀번호가 기존 비밀번호와 동일합니다."})
        else:
            raise ParseError("비밀번호를 다시 확인해주세요.")


# pick 수정
# (동일한 아이돌인지 비교 확인 추가)
class EditPick(APIView):

    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise NotFound

    def get(self, request):
        pick = request.user
        serializer = PickSerializer(pick)
        return Response(serializer.data)

    # pick 수정
    def put(self, request):
        pick = request.user

        serializer = PickSerializer(
            pick,
            data=request.data,
            partial=True,
        )

        if serializer.is_valid():
            updated_pick = serializer.save()
            return Response(PickSerializer(updated_pick).data)


# schedule 제보하기  :: OK
class AllReport(APIView):
    def get_object(self, pk):

        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise NotFound

    def get(self, request):

        all_reports = Report.objects.all()
        serializer = ReportDetailSerializer(all_reports, many=True)
        return Response(serializer.data, status=HTTP_200_OK)

    def post(
        self,
        request,
    ):

        serializer = ReportDetailSerializer(data=request.data)
        if serializer.is_valid():
            with transaction.atomic():

                report = serializer.save(
                    owner=request.user,
                )
                whoes = request.data.get("whoes")
                print(request.user.pick)
                if request.user.pick.pk not in whoes:
                    # if request.user.pick.pk
                    raise ParseError("참여자는 본인의 아이돌만 선택 가능합니다.")
                if not whoes:
                    raise ParseError("제보할 아이돌을 알려 주세요.")
                if len(set(whoes)) != 1:
                    raise ParseError("한명의 아이돌만 제보가 가능합니다.")
                if not isinstance(whoes, list):
                    if whoes:
                        raise ParseError("who_pk must be a list")
                    else:
                        raise ParseError(
                            "whoes report? Who should be required. not null"
                        )
                try:
                    idol = Idol.objects.get(pk=whoes[0])
                    print("idol_pk", idol)
                    report.whoes.add(idol)

                except Idol.DoesNotExist:
                    raise ParseError("선택하신 아이돌이 없어요.")

                serializer = ReportDetailSerializer(
                    report,
                    context={"request": request},
                )
                return Response(serializer.data, status=HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


class ReportDetail(APIView):
    def get_object(self, pk):
        try:
            return Report.objects.get(pk=pk)
        except Report.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        report = self.get_object(pk)
        serializer = ReportDetailSerializer(report)
        return Response(serializer.data, status=HTTP_200_OK)

    def put(self, request, pk):

        if not request.user.is_admin:
            raise PermissionDenied("권한 없음")
        else:
            report = self.get_object(pk)
            serializer = ReportDetailSerializer(
                report,
                data=request.data,
                partial=True,
            )
        if serializer.is_valid():
            updated_report = serializer.save()
            return Response(
                ReportDetailSerializer(updated_report).data, status=HTTP_200_OK
            )
        else:
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        reports = self.get_object(pk)

        if not request.user.is_admin:
            raise PermissionDenied

        reports.delete()

        return Response(status=HTTP_204_NO_CONTENT)


class Login(APIView):  # 관리자인지 아닌지 정보도 같이 전송할 것
    # {"email":"test@gmail.com", "password": "test123@E"}
    def post(self, request, format=None):
        email = request.data.get("email")
        password = request.data.get("password")
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise NotFound
        if not email or not password:
            raise ParseError("잘못된 정보를 입력하였습니다.")
        if user.check_password(password):
            login(request, user)
            serializer = TinyUserSerializers(user)
            return Response(serializer.data, status=HTTP_200_OK)
        return Response({"error": "Invalid credentials"}, status=HTTP_400_BAD_REQUEST)


# 로그아웃  :: OK
class Logout(APIView):  # OK
    permission_classes = [IsAuthenticated]

    def post(self, request):
        logout(request)
        return Response({"message": "See You Again~"}, status=HTTP_200_OK)

