from .models import UserCalendar
from .serializers import UserCalendarSerializer, UserDetailSerializer, MyScheduleSerializer
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.viewsets import ModelViewSet


class CalandarViewSet(ModelViewSet):
    queryset = UserCalendar.objects.all()
    serializer_class = MyScheduleSerializer
    # lookup_field = "pk"

class CalendarDetailViewSet(ModelViewSet):
    queryset = UserCalendar.objects.all()
    serializer_class = UserCalendarSerializer