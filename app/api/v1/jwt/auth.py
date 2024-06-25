from fastapi import APIRouter

from app import models
from app.api import deps
from app.core import exps

router = APIRouter()


@router.post('/token', response_model=models.AccessToken)
async def auth(
        data: models.UserCreate,
        service: deps.Service,
):
    """Retrieve new access token"""
    if user := await service.user.db_repository.retrieve_by_username(data.username):
        if not deps.pwd_context.verify(data.password, user.password):
            raise exps.USER_IS_CORRECT
    else:
        raise exps.USER_NOT_FOUND

    return models.AccessToken(
        token=service.jwt.encode_token({'id': user.id}, 1440)
    )
