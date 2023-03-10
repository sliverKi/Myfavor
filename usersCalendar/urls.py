from django.urls import path, include
from . import views


urlpatterns = [
    path("", views.UsersCalendar.as_view()),
    path("@<str:username>", views.UserCalendarDetail.as_view()),
    path("@<str:owner>", views.UserDetailCalendar.as_view()),
]
