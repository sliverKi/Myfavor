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
from users.serializers import TinyUserSerializers
from users.models import User
from .models import UserCalendar
from .serializers import MySerializer


# 유저 일정 조회(list) / user만 가능
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
                owner = request.user,
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
        return Response(serializer.data)

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






class PublicUser(APIView): # 본인만 수정 가능
    permission_classes = [IsAuthenticated]
    
    def get_object(self, request, nickname):
        if not request.user.is_authenticated:
            raise NotAuthenticated({"detail": "로그인이 필요합니다."})
    
    def get(self, request, nickname):

        try:
            user = User.objects.get(nickname=nickname)
        except User.DoesNotExist:
            raise NotFound()
        serializer = TinyUserSerializers(user)
        return Response(serializer.data)

    def put(self, request, nickname, pick):
        pass

    def delete(self, request, nickname):
        user = self.objects.get(nickname)
        if not request.user.is_authenticated:
            raise NotAuthenticated({"detail": "로그인이 필요합니다."})
        if user.nickname != request.user.nickname:
            raise PermissionDenied({"detail": "권한이 없습니다."})
        user.delete()
        return Response


class YearView(APIView):
    def get_object(self, pk):
        try:
            return UserCalendar.objects.get(pk=pk)
        except UserCalendar.DoesNotExist:
            raise NotFound
        
    def get(self, request, pk, year):
        calendar = self.get_object(pk=pk)
        schedule = calendar.objects.filter(when__year=year)
        serializer = MySerializer(
            schedule,
            many=True,
            # context={"request": request},
        )
        return Response(serializer.data)