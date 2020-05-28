from datetime import datetime, timedelta

import jwt
from django.conf import settings

from vending_machine.utils.constants import USER_LOGIN_COOKIE_EXPIRES


def generate_jwt(payload):
    """
    生成jwt
    :param payload: dict 载荷
    :param expiry: datetime 有效期
    :param secret: 密钥
    :return: jwt
    """
    now = datetime.utcnow()
    expiry = now + timedelta(hours=USER_LOGIN_COOKIE_EXPIRES)
    _payload = {'exp': expiry}
    _payload.update(payload)

    token = jwt.encode(_payload, settings.SECRET_KEY, algorithm='HS256')
    return token.decode()


def verify_jwt(token):
    """
    检验jwt
    :param token: jwt
    :param secret: 密钥
    :return: dict: payload
    """
    try:
        payload = jwt.decode(token,  settings.SECRET_KEY, algorithm=['HS256'])
    except jwt.PyJWTError:
        payload = None

    return payload
