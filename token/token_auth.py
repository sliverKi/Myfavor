import os, jwt, time, datetime
from django.contrib.auth import get_user_model
from rest_framework import exceptions

JWT_SECRET = os.environ.get("DJANGO_SECRET_KEY")
ALGORITHM = os.environ.get("JWT_ALGORITHM")

user_model = get_user_model()

def get_authorization_header(request):
    auth = request.META.get("HTTP_AUTHORIZATION")
    system_key = request.META.get("HTTP_SYSTEM_KEY")
    return [auth, system_key]


class CustomJwtTokenAuthentication():	
	keyword = "jwt"
    
    def authenticate(self, request):
        token = get_authorization_header(request)
        print(f"TOKEN : {token}")
        
        if not token or not system_key or ( system_key != os.environ.get("HTTP_SYSTEM_KEY")):
            raise exceptions.AuthenticationFailed("시스템 키가 없거나 사용자를 인증할 수 없습니다.")
        
        token = token.replace("jwt ", "")
        
        # 토큰 디코딩
        payload = jwt.decode(token, JWT_SECRET, algorithms=[ALGORITHM])

        # 토큰 만료 데이터 파싱
        expire = payload.get("exp")

        # 현재 시간
        cur_date = int(time.time())
        
        # 토큰 만료 처리
        if cur_date > expire:
            return None
        
        # 유저 객체
        user_id = payload.get("user_id")

        if not user_id:
            return None
        
        try:
            user = user_model.objects.get(pk=user_id)
        except user_model.DoesNotExist:
            raise exceptions.AuthenticationFailed("사용자가 존재하지 않습니다.")
        
        return (user, token)
        
    def authenticate_header(self, request):
        return self.keyword