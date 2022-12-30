# Authentication class가 반환하는 user가 바로 views에서 받게되는 user!
import jwt
from django.conf import settings
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from users.models import User


class TrustMeBroAuthentication(BaseAuthentication):
    def authenticate(self, request):
        username = request.headers.get("Trust-me")
        if not username:
            return None
        try:
            user = User.objects.get(username=username)
            return (user, None)  # 규칙!
        except User.DoesNotExist:
            raise AuthenticationFailed(f"No user {username}")


class JWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        token = request.headers.get("Jwt")
        if not token:  # token x, none반환하고 연결은 계속 유지
            return None
        decoded = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        pk = decoded.get("pk")
        if not pk:  # token o, but 그안에 pk 없다면 유효하지 않은 토큰!
            return AuthenticationFailed("Invalid Token")
        try:
            user = User.objects.get(pk=pk)
            return (user, None)  # request.user에서받게됨
        except User.DoesNotExist:
            raise AuthenticationFailed("User Not Found")
