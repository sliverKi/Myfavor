from django.urls import path, include
from . import views


urlpatterns = [
    path("", views.MyCalendar.as_view()),
    path("<int:pk>", views.MyCalendarDetail.as_view()),
    
    # 사용자 이름으로 조회 // 본인이 아니면 조회 불가
    
    # 사용자 이름 > year
    # 사용자 이름 > year/month
    # 사용자 이름 > year/month/day
    
    
    path("@<str:nickname>", views.PublicUser.as_view()),
    
    path("<int:pk>/<str:year>", views.YearView.as_view()),
    # path("<int:pk>/<str:year>/<str:month>", views.MonthView.as_view()),
    # path("<int:pk>/<str:year>/<str:month>/<str:day>", views.DayView.as_view()),
]