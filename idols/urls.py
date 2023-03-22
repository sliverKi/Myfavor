from django.urls import path
from . import views

urlpatterns = [
    path("", views.Idols.as_view()),  # idol-list  [ GET/  POST ]
    path("<int:pk>/", views.IdolDetail.as_view()),  # idol-detail  [GET /  POST, PUT, DELETE]
    path("<int:pk>/schedules/", views.IdolSchedule.as_view()),  # only one idol's schedule  [GET / POST]
    
    path("<int:pk>/schedules/<str:type>/",views.IdolSchedulesCategories.as_view()), #idol_schedules category [GET]
    path("<int:pk>/schedules/<str:type>/<str:year>/", views.IdolSchedulesYear.as_view()), # [GET]
    path("<int:pk>/schedules/<str:type>/<str:year>/<str:month>/", views.IdolSchedulesMonth.as_view()),  #[GET]
    path("<int:pk>/schedules/<str:type>/<str:year>/<str:month>/<str:day>/", views.IdolScheduelsDay.as_view()), #[GET]

    path("schedules/", views.Schedules.as_view()),  # all_schedules  [ GET, POST ]
    path("schedules/<int:pk>/", views.ScheduleDetail.as_view()),  # one_schedule  [PUT, DELETE]
    path("<int:pk>/photos", views.IdolPhotos.as_view()), #idol-profile img [POST]

]



