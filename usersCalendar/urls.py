from django.urls import path, include
from . import views


urlpatterns = [
    # 전체 조회 - [ get / post ]
    path("", views.MyCalendar.as_view()), # 내 일정 전체 조회
    
    # year - [ get ]
    path("<int:year>/", views.YearView.as_view()), # 내 일정 연도별 조회
    
    # month - [ get ]
    path("<int:year>/<int:month>/", views.MonthView.as_view()), # 내 일정 연도 - 월별 조회
    
    # day - [ post ]
    path("<int:year>/<int:month>/<int:day>/", views.DayView.as_view()), # 내 일정 연도- 월 - 일별 조회
    # day - [ get / post / delete ]
    path("<int:year>/<int:month>/<int:day>/<int:pk>", views.DayDetailView.as_view()), # 내 일정 연도/월/일 별 조회 / 수정 / 삭제
]