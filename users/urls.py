from django.urls import path
from . import views

urlpatterns=[
    
    path("", views.Users.as_view()),#userList[ X ]
    #path("me", views.Me.as_view()),#myProfile() 
    #path("ME/schedules", views.MySchedule.as_view()),
    
    path("log-in", views.LogIn.as_view()), # [ X ]
    path("log-out", views.LogOut.as_view()), # [ X ]
    path("change-password", views.ChangePassword.as_view()),#[ X ] 
 ]
