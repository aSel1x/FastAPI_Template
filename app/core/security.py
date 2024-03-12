from datetime import datetime, timedelta

from fastapi import HTTPException, status
from jose import JWTError, jwt
from passlib.context import CryptContext

from app import models

from . import settings

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

ALGORITHM = 'HS256'


def create_token(action: str, payload: dict, minutes: int) -> str:
    data = dict(
        action=action, payload=payload, exp=datetime.now() + timedelta(minutes=minutes)
    )
    encoded_jwt = jwt.encode(data, settings.APP_AUTH_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decode_token(token: str) -> dict | None:
    try:
        data = jwt.decode(token, settings.APP_AUTH_KEY, algorithms=[ALGORITHM])
        exp: float = data.get('exp')

        if datetime.fromtimestamp(exp) > datetime.now():
            return data
        return None
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail='Failed to parse token'
        )


def create_token_auth(payload: dict) -> models.TokenAuth:
    token_auth = create_token('token_auth', payload, 15)
    return models.TokenAuth(token_auth=token_auth)


def create_token_pair(payload: dict) -> models.TokenPair:
    token_long = create_token('token_long', payload, minutes=52560)
    token_short = create_token('token_short', payload, minutes=120)
    return models.TokenPair(token_long=token_long, token_short=token_short)
