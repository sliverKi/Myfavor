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
    permission_classes = IsAuthenticatedOrReadOnly

    def get(self, request):
        schedule = UserCalendar.objects.filter(user=request.user)
        serializer = UserCalendarSerializer(schedule, data=request.data, many=True)

        if serializer.is_valid():
            schedule = serializer.save()
            serializer = UserCalendarSerializer(schedule, many=True)
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


class UserCalendarDetail(APIView):
    def get_object(self, pk):
        try:
            return UserCalendar.objects.get(pk=pk)
        except UserCalendar.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        user_calendar = self.get_object(pk)
        serializer = UserCalendarSerializer(user_calendar)
        return Response(serializer.data)
