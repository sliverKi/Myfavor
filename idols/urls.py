from django.urls import path
from . import views

urlpatterns = [
    path("", views.Idols.as_view()),  # idol-list  [ GET/  POST ]
    path("<int:pk>/", views.IdolDetail.as_view()),  # idol-detail  [GET /  POST, PUT, DELETE]
    path("<int:pk>/schedules", views.IdolSchedule.as_view()),  # only one idol's schedule  [GET / POST]
    

    #안씀#
    path("schedules/", views.Schedules.as_view()),  # all_schedules  [ GET, POST ]
    path("schedules/<int:pk>", views.ScheduleDetail.as_view()),  # #one_schedule  [PUT, DELETE]
]

# <수정 보안 >
#관리자가 스케쥴 생성시 아이돌을 선택하면  해당하는 아이돌에도 자동으로 스케쥴에 추가되어야 함.
# 4/schedules -> post 수정 필요   추가하고 