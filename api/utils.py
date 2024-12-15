import jwt
from datetime import datetime, timedelta

from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth.models import User


def generate_jwt(user):
    payload = {
        'id':  user.id,
        'username': user.username,
        'iat': datetime.utcnow(),
        'exp': datetime.utcnow() + timedelta(hours=1)
    }

    token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')

    return token

def decode_jwt(token):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        user_id = payload.get('id')
        if not user_id:
            raise AuthenticationFailed("Token payload missing user ID")
    except jwt.ExpiredSignatureError:
        raise AuthenticationFailed("Token has expired")
    except jwt.InvalidTokenError:
        raise AuthenticationFailed("Invalid token")

    try:
        user = User.objects.get(id=user_id)
    except ObjectDoesNotExist:
        raise AuthenticationFailed("User does not exist")

    return user