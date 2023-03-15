from rest_framework.authtoken.views import obtain_auth_token
from django.urls import path
from . import views, JWTViews

urlpatterns = [
    path("", views.Users.as_view()), # 신규가입
    # path("admin", views.Admin.as_view()),  # adminProfile (pk:1)
    path("change-password", views.ChangePassword.as_view()),
    # path("signup",views.SignUp.as_view()),
    # path("signin",views.SignIn.as_view()),
    path("login", views.Login.as_view()),
    path("logout", views.Logout.as_view()),
    path("token-login",obtain_auth_token),
    # path("jwt-login",views.JWTLogin.as_view()),

    path("info/<int:pk>", views.UserDetail.as_view()),
    path("@<str:nickname>", views.PublicUser.as_view()), # nickname 으로 조회 (nickname의 값이 unique)
    
    path("register", JWTViews.RegisterView.as_view()),
    path("login-jwt", JWTViews.LoginView.as_view()),
    path("login-ing", JWTViews.UserView.as_view()),
    path("logout-jwt", JWTViews.LogoutView.as_view()),
    path("register", JWTViews.RegisterView.as_view()),

    ###################
    # path("ME/schedules", views.MySchedule.as_view()),  # - 수현
    # 
]
