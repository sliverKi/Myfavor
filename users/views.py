
from django.shortcuts import render
from django.conf import settings
from django.db import transaction
from django.contrib.auth import login, logout

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.status import (
    HTTP_200_OK, 
    HTTP_201_CREATED, 
    HTTP_204_NO_CONTENT, 
    HTTP_400_BAD_REQUEST
)
from rest_framework.exceptions import (
    NotFound,
    ParseError,
    PermissionDenied,
)
from .models import User, Report
from .serializers import (
    TinyUserSerializers,
    PrivateUserSerializer,
    UserDetailSerializer,
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
            return Response(serializer.data, status=HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
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
            return Response(serializer.data, status=HTTP_200_OK)
        else:
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
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
            return Response(serializer.data, status=HTTP_200_OK)
        else:
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
class PublicUser(APIView):
    # permission_classes = [IsAuthenticated]
    def get(self, request, username):
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise NotFound()
        serializer = PrivateUserSerializer(user)
        return Response(serializer.data, status=HTTP_200_OK)
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
            return Response(serializer.data, status=HTTP_200_OK)
        else:
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
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
        return Response(serializer.data, status=HTTP_200_OK)
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
            return Response(serializer.data, status=HTTP_200_OK)
        else:
            return Response({"detail": serializer.errors}, status=HTTP_400_BAD_REQUEST)
    def delete(self, request, pk):
        user = self.get_object(pk)
        user.delete()
        return Response(status=HTTP_200_OK)
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
            return Response(status=HTTP_200_OK)
        else:
            raise ParseError
        
class Login(APIView):#관리자인지 아닌지 정보도 같이 전송할 것 
    #{"email":"test@gmail.com", "password": "test123@E"}
    def post(self, request,  format=None):
       
        email = request.data.get("email")
        password = request.data.get("password")
        
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise NotFound     
               
        if not email or not password:
            raise ParseError("잘못된 정보를 입력하였습니다.")
        
        if user.check_password(password): #수정  
            login(request, user)
            return Response({'ok': 'Welcome'}, status=HTTP_200_OK)
        return Response({'error': 'Invalid credentials'}, status=HTTP_400_BAD_REQUEST)
        
class Logout(APIView):
    def post(self, request):
        logout(request)
        return Response(status=HTTP_200_OK)



class AllReport(APIView): #schedule 제보하기  :: OK
    def get_object(self, pk):  
        
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise NotFound 
    def get(self, request):
        
        all_reports = Report.objects.all() 
        serializer = ReportDetailSerializer(all_reports, many=True)
        return Response(serializer.data)
    
    def post(self, request):

        serializer = ReportDetailSerializer(data=request.data)
        if serializer.is_valid():
            with transaction.atomic():
               
                report=serializer.save(
                    owner=request.user,
                )
                whoes=request.data.get("whoes")
                if request.user.pick.pk not in whoes:            
                    raise ParseError("참여자는 본인의 아이돌만 선택 가능합니다.")
                if not whoes:
                    raise ParseError("제보할 아이돌을 알려 주세요.")
                if len(set(whoes))!=1:
                    raise ParseError("한명의 아이돌만 제보가 가능합니다.")
                if not isinstance(whoes, list):
                    if whoes:
                        raise ParseError("who_pk must be a list")
                    else:
                        raise ParseError("whoes report? Who should be required. not null")
                try:
                    idol=Idol.objects.get(pk=whoes[0])
                    print("idol_pk", idol)
                    report.whoes.add(idol)
                     
                except Idol.DoesNotExist:
                    raise ParseError("선택하신 아이돌이 없어요.")
                
                serializer=ReportDetailSerializer(
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
        report=self.get_object(pk)
        serializer=ReportDetailSerializer(report)
        return Response(serializer.data)


    def put(self, request, pk):
        
        if not request.user.is_admin:
            raise PermissionDenied("권한 없음")
        else:
            report = self.get_object(pk)
            serializer=ReportDetailSerializer(
                report, 
                data=request.data,
                partial=True,
            ) 
        if serializer.is_valid():
            updated_report=serializer.save()
            return Response(ReportDetailSerializer(updated_report).data)
        else:
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
        
    def delete(self, request, pk):
        reports = self.get_object(pk)

        if not request.user.is_admin:
            raise PermissionDenied

        reports.delete()

        return Response(status=HTTP_204_NO_CONTENT)