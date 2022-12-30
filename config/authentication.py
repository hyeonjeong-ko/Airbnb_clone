# Authentication class가 반환하는 user가 바로 views에서 받게되는 user!

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
