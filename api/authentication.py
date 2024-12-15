from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from .utils import decode_jwt


class JWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return None

        try:
            token = auth_header.split()[1]
        except IndexError:
            raise AuthenticationFailed("Invalid Authorization header format")

        user = decode_jwt(token)

        return (user, token)