import re
from django.shortcuts import render
from django.conf import settings
from django.db import transaction
from django.utils import timezone
from django.contrib.auth import authenticate, login, logout
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.status import HTTP_200_OK, HTTP_204_NO_CONTENT, HTTP_400_BAD_REQUEST
from rest_framework.exceptions import (
    NotFound,
    NotAuthenticated,
    ParseError,
    PermissionDenied,
)
from django.core.exceptions import ValidationError
from .models import User
from .serializers import (
    UserCreateSerializer,
    TinyUserSerializers,
    PrivateUserSerializer,
    UserDetailSerializer,
)


# 신규 유저 추가
class Register(APIView):
    
    def post(self, request):
        password = request.data.get("password")
        
        if not password:
            raise ParseError("비밀번호를 입력해 주세요.")
    
        serializer =  UserCreateSerializer(data=request.data)
    
        if serializer.is_valid():
            user = serializer.save()
            user.set_password(password)
            # set_password : 해쉬화 된 비밀번호 / #password : 실제 비밀번호
            user.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)  



class Users(APIView):
    #permission_classes = [IsAuthenticated]

    def get(self, request):  # 조회
        all_users = User.objects.all()  # 모든 Users 불러와
        serializer = TinyUserSerializers(
            all_users,
            many=True,
            context={"request": request},
        )
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
            return Response(serializer.errors)



class Admin(APIView):
    #permission_classes = [IsAuthenticated]

    # 관리자 정보 조회
    def get(self, request):
        user = request.user
        serializer = TinyUserSerializers(user)
        return Response(serializer.data)

    # 관리자 정보 update
    def put(self, request):
        user = request.user
        serializer = PrivateUserSerializer(
            user,
            data=request.data,
            partial=True,
        )

        if serializer.is_valid():
            user = serializer.save()
            serializer = PrivateUserSerializer(user)
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


class PublicUser(APIView):
    #permission_classes = [IsAuthenticated]

    def get(self, request, username):
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise NotFound()
        serializer = PrivateUserSerializer(user)
        return Response(serializer.data)

    def put(self, request, username):
        user = request.user
        serializer = PrivateUserSerializer(
            user,
            data=request.data,
            partial=True,
        )
        if serializer.is_valid():
            serializer.save()
            serializer = PrivateUserSerializer(user)
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


class UserDetail(APIView):
    #permission_classes = [IsAuthenticated]

    # 유저 정보 조회
    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        user = self.get_object(pk)
        serializer = UserDetailSerializer(user)

        return Response(serializer.data)

    # 유저 정보 update
    def put(self, request, pk):
        user = self.get_object(pk)
        serializer = UserDetailSerializer(
            user,
            data=request.data,
            partial=True,
        )

        if serializer.is_valid():
            user = serializer.save()
            serializer = UserDetailSerializer(user)
            return Response(serializer.data)
        else:
            return Response({"detail": serializer.errors})

    def delete(self, request, pk):
        user = self.get_object(pk)
        user.delete()
        return Response(status=status.HTTP_200_OK)



class ChangePassword(APIView):
    #permission_classes = [IsAuthenticated]

    # 유저 비번 update
    def put(self, request):
        user = request.user

        old_password = request.data.get("old_password")
        new_password = request.data.get("new_password")

        if not old_password or not new_password:
            raise ParseError

        if user.check_password(old_password):
            user.set_password(new_password)
            user.save()
            return Response(status=status.HTTP_200_OK)

        else:
            raise ParseError


class Login(APIView):
    def post(self, request):
        
        email = request.data.get("email")
        password = request.data.get("password")
        
        if not email or not password:
            raise ParseError("잘못된 정보를 입력하였습니다.")
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"error": "로그인 실패"})
        
        username = user.username
        # 로그인 시 필요조건 (email, password)
        user = authenticate(
            request,
            username=username,
            password=password,
        )
        if user:
            login(request, user)
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)

class Logout(APIView):
     def post(self, request):
        logout(request)
        return Response(status=status.HTTP_200_OK)


# #.env 설정

# import jwt
# from environ import Env
# from django.conf import settings

# # jwtLogin
# class Login(APIView):
#     def post(self, request):
#         username = request.data.get("username")
#         password = request.data.get("password")

#         if not username or not password:
#             raise ParseError

#         user = authenticate(
#             request,
#             username=username,
#             password=password,
#         )

#         if user:
#             token = jwt.encode(
#                 {"id": user.id, "username": user.username},
#                 settings.env("SECRET_KEY"),
#                 algorithm="HS256",
#             )
#             print(token)
#             return Response({"token": token})
# from django.contrib.auth import logout