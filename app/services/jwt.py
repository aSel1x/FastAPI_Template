import datetime as dt

from jose import JWTError, jwt
from jose.constants import ALGORITHMS

from app.core import exps, settings


class JWTService:
    secret_key: str = settings.APP_SECRET_KEY

    def decode_token(self, token: str) -> dict:
        try:
            payload = jwt.decode(
                token, self.secret_key, algorithms=[ALGORITHMS.HS256]
            )
        except JWTError:
            raise exps.TOKEN_INVALID

        exp = payload.get('exp')
        if exp and dt.datetime.now(dt.UTC).timestamp() > exp:
            raise exps.TOKEN_EXPIRED
        return payload.get('payload')

    def encode_token(self, payload: dict, minutes: int) -> str:
        claims = {
            'payload': payload,
            'exp': dt.datetime.now(dt.UTC) + dt.timedelta(minutes=minutes),
        }
        return jwt.encode(claims, self.secret_key, algorithm=ALGORITHMS.HS256)
