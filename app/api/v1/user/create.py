from fastapi import APIRouter

from app import models
from app.api import deps
from app.core import exps

router = APIRouter()


@router.post('/')
async def user_create(
        data: models.UserCreate,
        service: deps.Service
) -> models.UserBase:
    """Create new user"""

    if await service.user.db_repository.retrieve_by_username(data.username):
        raise exps.USER_EXISTS

    data.password = deps.pwd_context.hash(data.password)
    user = await service.user.db_repository.create(models.User(**data.model_dump()))
    return models.UserBase(**user.model_dump())
