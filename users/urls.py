
from rest_framework.authtoken.views import obtain_auth_token
from django.urls import path
from . import views, JWTViews
urlpatterns = [
    path("", views.Users.as_view()), # 신규가입
    path("userlist", views.AllUsers.as_view()),
    
    path("change-password/", views.ChangePassword.as_view()),
    path("login/", views.Login.as_view()),
    path("logout/", views.Logout.as_view()),
    path("token-login",obtain_auth_token),
    
    path("info/<int:pk>", views.UserDetail.as_view()), # pk로 조회 - admin의 정보 확인용 (모든 정보 보여주기)
    path("@<str:nickname>", views.PublicUser.as_view()), # nickname 으로 조회 (nickname의 값이 unique) - user의 정보 확인용 (정보 ㅈㅔ한적으로 보여주기
    
    path("reports/", views.AllReport.as_view()),
    path("reports/<int:pk>", views.ReportDetail.as_view()),
]
