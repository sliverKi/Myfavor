from django.urls import path
from . import views

urlpatterns = [
    path("", views.Idols.as_view()),  
    path("<int:pk>/", views.IdolDetail.as_view()),  
    path("<int:pk>/schedules/", views.IdolSchedule.as_view()),  
    
    path("<int:pk>/schedules/<str:type>/",views.IdolSchedulesCategories.as_view()), 
    path("<int:pk>/schedules/<str:type>/<str:year>/", views.IdolSchedulesYear.as_view()), 
    path("<int:pk>/schedules/<str:type>/<str:year>/<str:month>/", views.IdolSchedulesMonth.as_view()),  
    path("<int:pk>/schedules/<str:type>/<str:year>/<str:month>/<str:day>/", views.IdolScheduelsDay.as_view()), 

    path("schedules/", views.Schedules.as_view()), 
    path("schedules/<int:pk>/", views.ScheduleDetail.as_view()), 
    path("<int:pk>/photos/", views.IdolPhotos.as_view()),

]



