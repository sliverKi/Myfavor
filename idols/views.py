from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework.status import HTTP_204_NO_CONTENT, HTTP_400_BAD_REQUEST
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import Idol, Schedule
from .serializers import IdolsListSerializer, IdolDetailSerializer, ScheduleSerializer


# api/v1/idols/schedule (GET, POST)
# api/v1/idols/schedule/1(GET, PUT, DELETE)
class Idols(APIView):

    permission_classes=[IsAuthenticatedOrReadOnly]

    def get(self, request):
        all_idols=Idol.objects.all()
        serializer=IdolsListSerializer(all_idols, many=True)
        return Response(serializer.data)
    
    def post(self, request):#관리자만 허용하게 할 것 
      #만약 사용자가 관리자가 아니라면 허용하여서는 안됌
        #if request.user!=user.admin:
        #raise PermissionDenied

        serializer = IdolDetailSerializer(data=request.data)
        if serializer.is_valid():
            idol= serializer.save()
            return Response(IdolsListSerializer(idol).data)
        else:
            return Response(serializer.errors)
        

class IdolDetail(APIView):
    def get_object(self, pk):
        try:
            return Idol.objects.get(pk=pk)
        except Idol.DoesNotExist:
            raise NotFound
    
    def get(self, request, pk):
        idol=self.get_object(pk)
        serializer = IdolDetailSerializer(idol)
        return Response(serializer.data)
    



class IdolSchedule(APIView):
    def get_object(self, pk):
        try:
            return Idol.objects.get(pk=pk)
        except Idol.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        idol=self.get_object(pk)
        serializer=ScheduleSerializer(
            idol.idol_schedule.all(),
            many=True,
        )
        return Response(serializer.data)
 

class Schedules(APIView):
    def get(self, request):
        all_schedules=Schedule.objects.all()
        serializer=ScheduleSerializer(all_schedules, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = ScheduleSerializer(data=request.data)
        if serializer.is_valid():
            schedule= serializer.save()
            return Response(ScheduleSerializer(schedule).data)
        else:
            return Response(serializer.errors)    

class ScheduleDetail(APIView):

    def get_object(self, pk):
        try: 
            return Schedule.objects.get(pk=pk)
        except Schedule.DoesNotExist:
            raise NotFound
        
    def get(self, request, pk):
        schedule = self.get_object(pk)
        serializer = ScheduleSerializer(schedule)
        return Response(serializer.data,)
    
    def put(self, request, pk):
        schedule = self.get_object(pk)
        serializer=ScheduleSerializer(
            schedule,
            data=request.data,
            partial=True,
        )
        if serializer.is_valid():
            updated_schedule = serializer.save()
            return Response(ScheduleSerializer(updated_schedule).data)
        else:
            return Response(serializer.errors)
        
    def delete(self, request, pk):
        schedule = self.get_object(pk).delete()
        return Response(status=HTTP_204_NO_CONTENT)
