from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound,PermissionDenied,ParseError
from rest_framework.status import (
    HTTP_200_OK, 
    HTTP_201_CREATED, 
    HTTP_202_ACCEPTED, 
    HTTP_204_NO_CONTENT, 
    HTTP_400_BAD_REQUEST,
    HTTP_403_FORBIDDEN, 
    HTTP_404_NOT_FOUND 
)
from .models import Idol, Schedule
from .serializers import  IdolsListSerializer, IdolDetailSerializer, ScheduleSerializer, DateScheduleSerializer
from categories.serializers import CategorySerializer
from categories.models import Category
from media.serializers import PhotoSerializer
#3/17일 코드 수정
#3/21 code merge

class Idols(APIView):#idol-list 

    
    def get(self, request):#조회-> 누구나 가능  (OK)
        all_idols = Idol.objects.all()
        serializer = IdolsListSerializer(all_idols, many=True)
        return Response(serializer.data, status=HTTP_200_OK)

    def post(self, request):  #아이돌 리스트 생성 -> 관리자만 허용  (OK)
        
        if not request.user.is_admin: #관리자 아닌 경우 
            raise PermissionDenied
        serializer = IdolDetailSerializer(data=request.data)
        
        if serializer.is_valid():# 유효성 체크
            idol = serializer.save()
            return Response(IdolsListSerializer(idol).data, status=HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


class IdolDetail(APIView): #특정 idol-info 
    def get_object(self, pk): 
        try:
            return Idol.objects.get(pk=pk)
        except Idol.DoesNotExist:
            raise NotFound

    def get(self, request, pk): # 조회  (OK)
        idol = self.get_object(pk)
        serializer = IdolDetailSerializer(
            idol,
            context={"request": request},
            )
        return Response(serializer.data, status=HTTP_200_OK)
    
    def put(self, request, pk): #idol-info 수정 ~> 관리자만 가능 (OK)

        if not request.user.is_admin:
            raise PermissionDenied
        
        idol=self.get_object(pk)
        if request.user.is_admin:
            serializer=IdolDetailSerializer(
                idol,  # user-data
                data=request.data,
                partial=True,
            )

        if serializer.is_valid():
            idol_schedules=request.data.get("idol_schedules")
            if idol_schedules:
                if not isinstance(idol_schedules, list):
                    raise ParseError("Invalid schedules")
                idol.idol_schedules.clear()
                for idol_schedule_pk in idol_schedules: 
                    try:
                        schedule = Idol.objects.get(pk=idol_schedule_pk)
                        idol.idol_schedules.add(schedule)
                    except Schedule.DoesNotExist:
                        raise ParseError("Schedule not Found")
            updated_idol_schedules = serializer.save()
            return Response(IdolDetailSerializer(updated_idol_schedules).data, status=HTTP_202_ACCEPTED)
        else:
            return Response(status=HTTP_400_BAD_REQUEST)

    def delete(self, request, pk): #관리자만 삭제 가능  (OK)
        idol=self.get_object(pk)
       
        if request.user.is_admin==False: #관리자가 아닌 경우 
            raise PermissionDenied
        idol.delete()
        if idol.DoesNotExist: #찾는 아이돌이 없는 경우 
            return Response(status=HTTP_404_NOT_FOUND)    

class IdolSchedule(APIView):

    def get_object(self, pk):
        try:
            return Idol.objects.get(pk=pk)
        except Idol.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        idol = self.get_object(pk)
        serializer = ScheduleSerializer(
            
            idol.idol_schedules.all(),
            many=True,
        )
        return Response(serializer.data, status=HTTP_200_OK)

    
    def post(self, request,pk): # (OK)
        
        print("post start")
        serializer=ScheduleSerializer(data=request.data)
        if not request.user.is_admin:
            raise PermissionDenied
        
        else:
            serializer = ScheduleSerializer(data=request.data)
            if serializer.is_valid():
                schedule = serializer.save()
                print(schedule)
        # 1. ScheduleType 에 있는 필드가 Category에 없는 경우, 유저가 입력한 내용을 새롭게 db에 생성(ok)     
                #ScheduleType_data=request.data.get("ScheduleType")
                
                try: #카테고리가 있는 경우 > type > content 
                    #print(1)
                    ScheduleType_data=request.data.get("ScheduleType")
                    schedule_type=Category.objects.get(type=ScheduleType_data)
                    #print(schedule_type)
                    #ScheduleContent_data=request.data.get("content")
                    #schedule_content=Category.objects.filter(type=ScheduleType_data, content=ScheduleContent_data).first()
                    
                    if not schedule_content:
                        schedule_content=Category.objects.create(type=ScheduleType_data)#, content=ScheduleContent_data)
                    schedule.ScheduleType = schedule_type
                    schedule.ScheduleContent = schedule_content
                    schedule.save()
                    
                except Category.DoesNotExist:
                    #print(2)
                    category_serializer=CategorySerializer(data=ScheduleType_data)#카테고리 시리얼라이즈를 이용해 데이터 번역
                    
                    if category_serializer.is_valid():#유효성 체크
                        schedule_type=category_serializer.save()#저장
                    else:
                        return Response(category_serializer.errors, status=HTTP_400_BAD_REQUEST)
                    schedule.ScheduleType=schedule_type#schedule_type을 schedule model의 ScheduleType변수에 할당
                    schedule.save()  #유저가 입력한 내용을 schedule에 저장
                    #print(ScheduleType success) 
        
        # 2. participant 에 있는 idol의 idol_schedules 필드에 자동으로 schedule추가(OK)
        # 3. particioant에 아이돌 이름을 입력하면, 해당하는 아이돌들이 participant field에  자동으로 선택되어 질 것(ok)
                for participant_data in request.data.get("participant"):
                    #if participant_data==None:
                        #return Response(status=HTTP_404_NOT_FOUND)
                    try:
                        idol_name_kr=participant_data.get("idol_name_kr")
                        idol=Idol.objects.get(idol_name_kr=idol_name_kr)
                        schedule.participant.add(idol)
                        
                    except Idol.DoesNotExist:#아이돌이 없는 경우 :: 새로운 아이돌 만듦
                        idol_serializer=IdolDetailSerializer(data=participant_data)
                        if idol_serializer.is_valid():
                            idol=idol_serializer.save()
                        else:
                            return Response(idol_serializer.errors, status=HTTP_404_NOT_FOUND)
                    idol.idol_schedules.add(schedule)
                    #print("schedule add success")
                return Response(ScheduleSerializer(schedule).data, status=HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
    
class IdolSchedulesCategories(APIView):# 특정 idol의 idol_schedule을 scheduelType의 카테고리별로 나눔 
    
    def get_object(self, pk):
        try:
            return Idol.objects.get(pk=pk)        
        except Idol.DoesNotExist:
            raise NotFound
    
        
    def get(self, request, pk,  type):
        
        idol=self.get_object(pk)
        schedules=idol.idol_schedules.filter(ScheduleType__type=type).order_by("when")
        
        #filter_schedules=[s for s in schedules if s.ScheduleType and s.ScheduleType.type==type]
        filter_schedules=[]
        for s in schedules:
            if s.ScheduleType and s.ScheduleType.type==type:
                filter_schedules.append(s)
        #print("filter_schedules",filter_schedules)#category sort

        serializer=ScheduleSerializer(filter_schedules, many=True)

        return Response(serializer.data, status=HTTP_200_OK)


class IdolSchedulesYear(APIView):
    def get_object(self, pk):
        try:
            return Idol.objects.get(pk=pk)
        except Idol.DoesNotExist:
            return NotFound
    def get(self, request, pk, type, year):
        idol=self.get_object(pk=pk)
        schedules=idol.idol_schedules.filter(ScheduleType__type=type, when__year=year)
        serializer=DateScheduleSerializer(schedules, many=True)
        return Response(serializer.data, status=HTTP_200_OK) 

class IdolSchedulesMonth(APIView):
    def get_object(self, pk):
        try:
            return Idol.objects.get(pk=pk)
        except Idol.DoesNotExist:
            return NotFound
    def get(self, request, pk, type, year, month):
        idol=self.get_object(pk=pk)
        schedules=idol.idol_schedules.filter(ScheduleType__type=type, when__year=year, when__month=month)
        serializer=DateScheduleSerializer(schedules, many=True)
        return Response(serializer.data, status=HTTP_200_OK) 


class IdolScheduelsDay(APIView):
    def get_object(self, pk):
        try:
            return Idol.objects.get(pk=pk)
        except Idol.DoesNotExist:
            return NotFound
    def get(self, request, pk, type, year, month, day):
        idol=self.get_object(pk=pk)
        schedules=idol.idol_schedules.filter(ScheduleType__type=type, when__year=year, when__month=month, when__day=day)
        
        serializer=DateScheduleSerializer(schedules, many=True)
        return Response(serializer.data, status=HTTP_200_OK) 
        

        





class Schedules(APIView): #'아이돌 구분 없이' 현재 저장되어진 스케줄들을 모두 보여줌
    def get(self, request):
        all_schedules = Schedule.objects.all()
        serializer = ScheduleSerializer(all_schedules, many=True)
        return Response(serializer.data)

    def post(self, request):
        print("post start")
        if not request.user.is_admin:
            raise PermissionDenied
        else:
            serializer = ScheduleSerializer(data=request.data)
            if serializer.is_valid():
                schedule = serializer.save()
                return Response(ScheduleSerializer(schedule).data, HTTP_201_CREATED )
            else:
                return Response(serializer.errors, HTTP_403_FORBIDDEN)


class ScheduleDetail(APIView): # 특정 schedule의 pk로 들어감. 
                               # if 삭제) db에서도 삭제되고 해당 스케줄을 갖고 있는 아이돌의 스케줄 항목에서도 삭제됨.
    def get_object(self, pk):
        try:
            return Schedule.objects.get(pk=pk)
        except Schedule.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        schedule = self.get_object(pk)
        serializer = ScheduleSerializer(schedule)
        return Response(serializer.data, status=HTTP_200_OK)

    def put(self, request, pk):
        
        if not request.user.is_admin:
            raise PermissionDenied
        
        if request.user.is_admin:
            schedule = self.get_object(pk)
            serializer = ScheduleSerializer(
                schedule,
                data=request.data,
                partial=True,
            )
            if serializer.is_valid():
                updated_schedule = serializer.save()
                return Response(ScheduleSerializer(updated_schedule).data, status=HTTP_202_ACCEPTED)
            else:
                return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):#(OK)

        schedule = self.get_object(pk)
        if not request.user.is_admin:
            return PermissionDenied
        schedule.delete()
        return Response(status=HTTP_204_NO_CONTENT)
    

class IdolPhotos(APIView):
    def get_object(self, pk):
        try:
            return Idol.objects.get(pk=pk)    
        except Idol.DoesNotExist:
            raise NotFound
    def post(self, request, pk):
        idol =self.get_object(pk)
        if not request.user.is_admin:   
            raise PermissionDenied
        serializer=PhotoSerializer(data=request.data)
        if serializer.is_valid():
            photo=serializer.save(idol=idol)
            serializer=PhotoSerializer(photo)
            return Response(serializer.data, status=HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

