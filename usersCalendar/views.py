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
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_403_FORBIDDEN
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


# 년도별 조회
# class YearView(APIView):

#     permission_classes = [IsAuthenticated]

#     def get_object(self, year):
#         try:
#             return UserCalendar.objects.filter(when__year=year)
#         except User.DoesNotExist:
#             raise NotFound

#     def get(self, request, year):

#         calendar = self.get_object(year)
#         print(calendar)
#         serializer = DateSerializer(
#             calendar,
#             many=True,
#             context={"request": request},
#         )

#         return Response(serializer.data, status=HTTP_200_OK)


class YearView(APIView):

    permission_classes = [IsAuthenticated]

    def get_object(self, year):
        # Retrieve the calendars for the specified year and requesting user
        calendars = UserCalendar.objects.filter(
            when__year=year,
            owner=self.request.user,
        )

        if not calendars:
            raise NotFound

        return calendars

    def get(self, request, year):
        calendars = self.get_object(year)

        serializer = DateSerializer(
            calendars,
            many=True,
            context={"request": request},
        )

        return Response(serializer.data, status=HTTP_200_OK)


# 월별 조회
class MonthView(APIView):

    permission_classes = [IsAuthenticated]

    def get_object(self, year, month):
        # Retrieve the calendars for the specified year and requesting user
        calendars = UserCalendar.objects.filter(
            when__year=year,
            when__month=month,
            owner=self.request.user,
        )

        if not calendars:
            raise NotFound

        return calendars

    def get(self, request, year, month):

        calendar = self.get_object(year, month)
        print(calendar)
        serializer = DateSerializer(
            calendar,
            many=True,
            context={"request": request},
        )

        return Response(serializer.data, status=HTTP_200_OK)


# 일별 조회 [get / post]
class DayView(APIView):

    permission_classes = [IsAuthenticated]

    def get_object(self, year, month, day):
        # Retrieve the calendars for the specified year and requesting user
        calendars = UserCalendar.objects.filter(
            when__year=year,
            when__month=month,
            when__day=day,
            owner=self.request.user,
        )

        if not calendars:
            raise NotFound

        return calendars

    def get(self, request, year, month, day):

        calendar = self.get_object(year, month, day)

        serializer = DateSerializer(
            calendar,
            many=True,
            context={"request": request},
        )

        return Response(serializer.data, status=HTTP_200_OK)

    # 당일 일정 작성
    def post(self, request, year, month, day):
        serializer = MySerializer(data=request.data)
        print("day", day)
        if serializer.is_valid():
            schedule = serializer.save(
                owner=request.user,
            )
            print("day", day)
            return Response(MySerializer(schedule).data)
        else:
            return Response(serializer.errors)


# 당일 일정 하나씩 pk 번호로 조회 [get / put / delete]
class DayDetailView(APIView):
    def get_object(self, year, month, day, pk):
        # Retrieve the calendars for the specified year and requesting user
        calendars = UserCalendar.objects.filter(
            when__year=year,
            when__month=month,
            when__day=day,
            owner=self.request.user,
            pk=pk,
        )

        if not calendars:
            raise NotFound

        return calendars

    def get(self, request, year, month, day, pk):

        if calendar.user != self.request.user:
            raise PermissionDenied(status=HTTP_403_FORBIDDEN)

        calendar = self.get_object(year, month, day, pk)

        serializer = DateSerializer(
            calendar,
            many=True,
            context={"request": request},
        )

        return Response(serializer.data, status=HTTP_200_OK)

    # 당일 일정 수정
    def put(self, request, year, month, day, pk):
        calendar = self.get_object(year, month, day, pk).get()
        serializer = DateSerializer(calendar, data=request.data, partial=True)
        if serializer.is_valid():
            calendar = serializer.save(user=request.user)
            serializer = DateSerializer(calendar)
            return Response(serializer.data, status=HTTP_200_OK)
        else:
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

    # 당일 일정 삭제
    def delete(self, request, year, month, day, pk):
        schedule = self.get_object(year, month, day, pk)
        schedule.delete()
        return Response({"message": "일정이 삭제되었습니다."}, status=HTTP_200_OK)
