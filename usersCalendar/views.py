from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import (
    IsAuthenticated,
)
from rest_framework.exceptions import (
    NotAuthenticated,
    PermissionDenied,
    ParseError,
    NotFound,
)
from rest_framework.validators import ValidationError
from rest_framework.status import HTTP_200_OK
from users.serializers import TinyUserSerializers
from users.models import User
from .models import UserCalendar
from .serializers import MySerializer, DateSerializer


# 유저 일정 조회(list) / 본인만 가능
class MyCalendar(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        all_schedule = UserCalendar.objects.filter(owner=request.user)
        serilaizer = MySerializer(
            all_schedule,
            many=True,
            context={"request": request},
        )
        return Response(serilaizer.data)

    # 유저 일정 입력
    def post(self, request):
        serializer = MySerializer(data=request.data)

        if serializer.is_valid():
            schedule = serializer.save(
                owner=request.user,
            )
            return Response(MySerializer(schedule).data)
        else:
            return Response(serializer.errors)


# 유저 일정 조회, 수정, 삭제 / user만 가능
# 일정을 pk로 자세히 조회
class MyCalendarDetail(APIView):

    permission_classes = [IsAuthenticated]

    def get_object(self, pk, user):
        try:
            return UserCalendar.objects.get(pk=pk, owner=user)
        except UserCalendar.DoesNotExist:
            raise NotFound

    # 유저 일정 조회
    def get(self, request, pk):
        schedule = self.get_object(pk, request.user)
        serializer = MySerializer(
            schedule,
            context={"request": request},
        )
        return Response(serializer.data, status=HTTP_200_OK)

    # 유저 일정 수정
    def put(self, request, pk):
        schedule = self.get_object(pk, request.user)
        serializer = MySerializer(
            schedule,
            data=request.data,
            partial=True,
        )
        if serializer.is_valid():
            schedule = serializer.save()
            serializer = MySerializer(schedule)
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

    # 유저 일정 삭제
    def delete(self, request, pk):
        schedule = self.get_object(pk, request.user)
        schedule.delete()
        return Response({"message": "일정이 삭제되었습니다."})


class YearView(APIView):

    permission_classes = [IsAuthenticated]

    def get_object(self, year):
        try:
            return UserCalendar.objects.filter(when__year=year)
        except User.DoesNotExist:
            raise NotFound

    def get(self, request, year):

        calendar = self.get_object(year)
        print(calendar)
        serializer = DateSerializer(
            calendar,
            many=True,
            context={"request": request},
        )

        return Response(serializer.data, status=HTTP_200_OK)


class MonthView(APIView):

    permission_classes = [IsAuthenticated]

    def get_object(self, year, month):
        try:
            return UserCalendar.objects.filter(when__year=year, when__month=month)
        except User.DoesNotExist:
            raise NotFound

    def get(self, request, year, month):

        calendar = self.get_object(year, month)
        print(calendar)
        serializer = DateSerializer(
            calendar,
            many=True,
            context={"request": request},
        )

        return Response(serializer.data, status=HTTP_200_OK)


class DayView(APIView):

    permission_classes = [IsAuthenticated]

    def get_object(self, year, month, day):
        try:
            return UserCalendar.objects.filter(
                when__year=year, when__month=month, when__day=day
            )
        except User.DoesNotExist:
            raise NotFound

    def get(self, request, year, month, day):

        calendar = self.get_object(year, month, day)
        
        serializer = DateSerializer(
            calendar,
            many=True,
            context={"request": request},
        )

        return Response(serializer.data, status=HTTP_200_OK)

    def post(self, request, year, month, day):
        serializer = MySerializer(data=request.data)
        print("day",day)
        if serializer.is_valid():
            schedule = serializer.save(
                owner=request.user,
            )
            print("day",day)
            return Response(MySerializer(schedule).data)
        else:
            return Response(serializer.errors)

    def put(self, request, year, month, day):
        schedule = self.get_object(year, month, day)
        serializer = MySerializer(
            schedule,
            data=request.data,
            partial=True,
        )
        if serializer.is_valid():
            schedule = serializer.save()
            serializer = MySerializer(schedule)
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

    def delete(self, request, year, month, day):
        schedule = self.get_object(year, month, day)
        schedule.delete()
        return Response({"message": "일정이 삭제되었습니다."})
