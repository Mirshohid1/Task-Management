import jwt
from datetime import datetime, timedelta

from django.conf import settings


def generate_jwt(user):
    payload = {
        'id':  user.id,
        'username': user.username,
        'iat': datetime.utcnow(),
        'exp': datetime.utcnow() + timedelta(hours=1)
    }

    token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')

    return token