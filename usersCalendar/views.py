from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import (
    NotFound,
    NotAuthenticated,
    ParseError,
    PermissionDenied,
)

from .models import UserCalendar
from .serializers import UserCalendarSerializer


class UsersCalendar(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        all_calendars = UserCalendar.objects.all()
        serializer = UserCalendarSerializer(
            all_calendars,
            many=True,
        )
        return Response(serializer.data)

    def post(self, request):
        serializer = UserCalendarSerializer(data=request.data)
        if serializer.is_valid():
            userCalendar = serializer.save()
            return Response(serializer.data(userCalendar).data)
        else:
            return Response(serializer.errors)


# 유저 일정 조회 (owner로 조회)
class UserCalendarDetail(APIView):

    permission_classes = [IsAuthenticated]

    def get_object(self, request, owner):
        try:
            return UserCalendar.objects.get(owner=owner)
            # user_calendar = self.objects.get(owner=owner)
        except UserCalendar.DoesNotExist:
            raise NotFound()
        
    def get(self, request, owner):
        user_calendar = self.get_object(owner)
        serializer = UserCalendarSerializer(user_calendar)
        
        return Response(serializer.data)

    # 유저 캘린더 업데이트
    def put(self, request, owner):
        user_calendar = request.user_calendar
        serializer = UserCalendarSerializer(
            user_calendar,
            data=request.data,
            partial=True,
        )
        if serializer.is_valid():
            serializer.save()
            serializer = UserCalendarSerializer(user_calendar)
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

    def delete(self, request, owner):
        user_calendar = self.get_object(owner)
        user_calendar.delete()
        return Response(status=status.HTTP_200_OK)

class UserDetailCalendar(APIView):
    def get(self, request, username):
        calendar = UserCalendar.objects.get(username=username)
        serializer = UserCalendarSerializer(calendar)
        return Response(serializer.data)