from typing import Annotated

from fastapi import Depends
from fastapi.security import APIKeyHeader
from passlib.context import CryptContext

from app import models
from app.core import exps
from app.core.db import Database as __Database
from app.core.service import Service as __Service

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
Service = Annotated[__Service, Depends(__Service)]
Database = Annotated[__Database, Depends(__Database.get)]


async def get_current_user(
    token: Annotated[str, Depends(APIKeyHeader(name='access-token'))],
    db: Database,
    service: Service,
) -> models.User:
    payload = service.jwt.decode_token(token)
    if not (user := await db.user.retrieve_one(ident=payload.get('id'))):
        raise exps.USER_NOT_FOUND
    return user


CurrentUser = Annotated[models.User, Depends(get_current_user)]
