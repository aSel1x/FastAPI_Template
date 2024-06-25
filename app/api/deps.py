from typing import Annotated

from fastapi import BackgroundTasks, Depends
from fastapi.security import APIKeyHeader
from passlib.context import CryptContext
from sqlmodel.ext.asyncio.session import AsyncSession

from app import models
from app.core import exps
from app.core.db import SessionLocal
from app.service import Service as __Service

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


async def get_session() -> AsyncSession:
    async with SessionLocal() as session:
        yield session


async def get_service(
        session: Annotated[SessionLocal, Depends(get_session)],
        background: Annotated[BackgroundTasks, BackgroundTasks()]
) -> __Service:
    return Service(session, background)

Service = Annotated[__Service, Depends(get_service)]


async def get_current_user(
    token: Annotated[str, Depends(APIKeyHeader(name='access-token'))],
    service: Annotated[Service, Depends(get_service)],
) -> models.User:
    payload = service.jwt.decode_token(token)
    if not (user := await service.user.db_repository.retrieve_one(ident=payload.get('id'))):
        raise exps.USER_NOT_FOUND
    return user

CurrentUser = Annotated[models.User, Depends(get_current_user)]
