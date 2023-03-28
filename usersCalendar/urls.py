from django.urls import path
from . import views


urlpatterns = [
   
    path("", views.MyCalendar.as_view()), # 내 일정 전체 조회
    path("<int:year>/", views.YearView.as_view()), # 내 일정 연도별 조회
    path("<int:year>/<int:month>/", views.MonthView.as_view()), # 내 일정 연도 - 월별 조회    
    path("<int:year>/<int:month>/<int:day>/", views.DayView.as_view()), # 내 일정 연도- 월 - 일별 조회
    path("<int:year>/<int:month>/<int:day>/<int:pk>/", views.DayDetailView.as_view()), # 내 일정 연도/월/일 별 조회 / 수정 / 삭제

]