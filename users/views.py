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
from .models import User, Report
from .serializers import (
    TinyUserSerializers,
    PrivateUserSerializer,
    UserDetailSerializer,
    ReportSerializer,
    ReportDetailSerializer
)
from idols.serializers import ScheduleSerializer
from idols.models import Idol
# 신규 유저 추가
class Users(APIView): # OK
    def post(self, request):
        serializer = PrivateUserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            serializer = PrivateUserSerializer(user)
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
class AllUsers(APIView):
    
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
    
    # 관리자 정보 조회
    def get(self, request):
        user = request.user
        serializer = PrivateUserSerializer(user)
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
    # permission_classes = [IsAuthenticated]
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
    # permission_classes = [IsAuthenticated]
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
    # permission_classes = [IsAuthenticated]
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
        
class Login(APIView):#관리자인지 아닌지 정보도 같이 전송할 것 
    def post(self, request,  format=None):
       
        email = request.data.get("email")
        password = request.data.get("password")
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise NotFound            
        # print("user", user.email)
#{"username":"test@gmail.com", "password": "test123@E"}
        if not email or not password:
            raise ParseError("잘못된 정보를 입력하였습니다.")
        if user.check_password(password):
            login(request, user)
            return Response({'ok': 'Welcome'}, status=status.HTTP_200_OK)
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)
        # 로그인 시 필요조건 (email, password)
      
        # user = authenticate(
        #     request,
        #     email=email,
        #     password=password,
        # )
        # print("email", email)
        # print("password", password)
        # if user:
        #     login(request, user)
        #     return Response(status=status.HTTP_200_OK)
        # else:
        #     return Response(status=status.HTTP_403_FORBIDDEN)
class Logout(APIView):
    def post(self, request):
        logout(request)
        return Response(status=status.HTTP_200_OK)





class AllReport(APIView): #schedule 제보하기  :: GET(user가 제보한 내용 ), POST(제보하기), PUT(제보 수정하기), DELETE(제보 삭제)d
    def get_object(self, pk): ##put 로직 추가 delete 할 필요 없음 
        
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise NotFound 
    def get(self, request):
        
        all_reports = Report.objects.all()#user가 작성한 것만 필터링 
        serializer = ReportDetailSerializer(all_reports, many=True)
        return Response(serializer.data)
    
    def post(self, request):
       
        serializer = ReportDetailSerializer(data=request.data)
        if serializer.is_valid():
            report=serializer.save(
                owner=request.user
            ##whoes:; add (수정 필요)
                )
            serializer = ReportSerializer(report)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
   
        
    
    
"""class ReportDetail(APIView):

    def get_report(self, pk):
        try:
            return Report.objects.get(pk=pk)
        except Report.DoesNotExist:
            raise NotFound    

    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise NotFound    
        
    def get(self, request, pk, report_pk):(수정 필요)
        reports = self.get_report(report_pk)
        if reports.owner == self.get_report(pk):
            return Response(ReportSerializer(reports).data)
        else:
            raise NotFound


    def put(self, request, pk, report_pk):
        user = self.get_object(pk)
        try:
            report = Report.objects.get(pk=report_pk, owner=user)
        except Report.DoesNotExist:
            raise NotFound

        serializer = ReportSerializer(report, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk, report_pk):
        reports = self.get_report(report_pk)

        if reports.user.pk != request.user.pk:
            raise PermissionDenied

        reports.delete()

        return Response(status=204)
"""

        