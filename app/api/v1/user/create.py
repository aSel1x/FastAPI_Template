from fastapi import APIRouter

from app import models
from app.api import deps
from app.core import exps

router = APIRouter()


@router.post('/')
async def user_create(
        data: models.UserCreate,
        db: deps.Database,
) -> models.UserBase:
    """Create new user"""

    if await db.user.retrieve_by_username(data.username):
        raise exps.USER_EXISTS

    data.password = deps.pwd_context.hash(data.password)
    user = await db.user.create(models.User(**data.model_dump()))
    return models.UserBase(**user.model_dump())
