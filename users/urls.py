
from rest_framework.authtoken.views import obtain_auth_token
from django.urls import path

from . import views


urlpatterns = [
    path("", views.NewUsers.as_view()), # 신규 가입 ( 첫 화면 )
    path("list/", views.AllUsers.as_view()),  # userList[ admin ]
    
    path("mypage/", views.MyPage.as_view()),  # userProfile[ user ] - user용 / user의 정보를 수정할 수 있는 페이지
    path("<int:pk>/", views.UserDetail.as_view()), # pk로 조회 - admin의 정보 확인용 (모든 정보 보여주기)
    
    path("reports/", views.AllReport.as_view()),
    path("reports/<int:pk>/", views.ReportDetail.as_view()),
    
    path("edit/pick/", views.EditPick.as_view()),  # pk로 수정 - user의 정보 수정 (닉네임, 이메일, 비밀번호
    path("edit/password/", views.EditPassword.as_view()),  # 비밀번호 변경
    
    path("login/", views.Login.as_view()), # 로그인
    path("logout/", views.Logout.as_view()), # 로그아웃
    
]
#user-profile을 받는 url 하나 만들것 
