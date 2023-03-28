from django.urls import path

from . import views


urlpatterns = [

    path("", views.NewUsers.as_view()),  
    path("list/", views.AllUsers.as_view()),  
    path("mypage/", views.MyPage.as_view()),  
    path("<int:pk>/", views.UserDetail.as_view()),  
    path("reports/", views.AllReport.as_view()),
    path("reports/<int:pk>/", views.ReportDetail.as_view()),
    path("edit/pick/", views.EditPick.as_view()),  
    path("edit/password/", views.EditPassword.as_view()),  
    path("login/", views.Login.as_view()),  
    path("logout/", views.Logout.as_view()),  

]

