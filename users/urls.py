from rest_framework.authtoken.views import obtain_auth_token
from django.urls import path
from . import views

urlpatterns = [
    path("", views.Users.as_view()), # 신규가입
    path("userlist", views.AllUsers.as_view()),  # userList[ o ]
    path("admin", views.Admin.as_view()),  # adminProfile (pk:1)
    path("change-password", views.ChangePassword.as_view()),
    # path("login", views.Login.as_view()),  # [ X ]
    # path("logout", views.Logout.as_view()),  # [ X ]
    path("login", views.Login.as_view()),
    path("logout", views.Logout.as_view()),
    path("token-login",obtain_auth_token),
    path("jwt-login",views.JWTLogin.as_view()),  
    path("info/<int:pk>", views.UserDetail.as_view()),
    path("@<str:username>", views.PublicUser.as_view()),
    # path("register", views.Register.as_view()),
    ###################
    # path("ME/schedules", views.MySchedule.as_view()),  # - 수현
    # --
]
