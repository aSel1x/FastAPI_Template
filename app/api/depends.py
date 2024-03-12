from typing import AsyncGenerator

from fastapi import BackgroundTasks, Depends, HTTPException, Request, status
from sqlmodel.ext.asyncio.session import AsyncSession

from app import models
from app.core import SessionLocal, security
from app.service import Service


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with SessionLocal() as session:
        yield session


async def get_service(
        session: SessionLocal = Depends(get_session),
        background: BackgroundTasks = BackgroundTasks()
) -> Service:
    return Service(session, background)


async def get_current_user(
    request: Request, service: Service = Depends(get_service)
) -> models.User:
    if not (token_short := request.cookies.get('_token_short')):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Short token not transferred',
        )

    if not (token_short_data := security.decode_token(token_short)):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Your short token have expired',
        )

    if token_short_data.get('action') != 'token_short':
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='You did not transfer a short token',
        )

    if not (user := await service.user.db_repository.get(
        payload.get('id') if isinstance((payload := token_short_data.get('payload')), dict) else None
    )):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail='User not found'
        )

    return user
