from fastapi import APIRouter, Depends, HTTPException, status

from app import models
from app.core import security
from app.service import Service

from ... import depends

router = APIRouter()


@router.get('/auth/')
async def get_token_auth(
    username: str,
    password: str,
    service: Service = Depends(depends.get_service),
) -> models.TokenAuth:
    if not (user := await service.user.db_repository.get_by_username(username, password)):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='A user not yet been registered',
        )
    token_auth = security.create_token_auth({'id': user.id})
    return token_auth
