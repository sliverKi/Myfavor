from rest_framework.decorators import APIView
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from users.serializers import PrivateUserSerializer
from django.contrib.auth import authenticate, login, logout
from .models import User
import jwt, datetime


class RegisterView(APIView):  # 회원가입
    def post(self, request):
        serializer = PrivateUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class LoginView(APIView):  # 로그인
    def post(self, request):
        email = request.data["email"]
        password = request.data["password"]

        # email is unique,
        user = User.objects.filter(email=email).first()
        serialize_user = PrivateUserSerializer(user)
        json_user = JSONRenderer().render(serialize_user.data)

        if user is None:
            raise AuthenticationFailed("User does not found!")

        # is same?
        if not user.check_password(password):
            raise AuthenticationFailed("Incorrect password!")

        ## JWT 구현 부분
        payload = {
            "id": user.id,
            "exp": datetime.datetime.now() + datetime.timedelta(minutes=60),
            "iat": datetime.datetime.now(),
        }

        token = jwt.encode(payload, "secretJWTkey", algorithm="HS256")

        res = Response()
        res.set_cookie(key="jwt", value=token, httponly=True)
        res.data = {"jwt": token}

        return res


# 로그인 유지
class UserView(APIView):
    def get(self, request):
        token = request.COOKIES.get("jwt")

        if not token:
            raise AuthenticationFailed("UnAuthenticated!")

        try:
            payload = jwt.decode(token, "secretJWTkey", algorithms=["HS256"])

        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("UnAuthenticated!")

        user = User.objects.filter(id=payload["id"]).first()
        serializer = PrivateUserSerializer(user)

        return Response(serializer.data)


# 로그아웃
class LogoutView(APIView):
    def post(self, request):
        logout(request)
        logout.delete_cookie("jwt")
        return Response({"See You Again!"})