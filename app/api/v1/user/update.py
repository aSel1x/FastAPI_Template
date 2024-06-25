from fastapi import APIRouter

from app import models
from app.api import deps

router = APIRouter()


@router.patch('/')
async def user_update(
        user: models.UserCreate,
        c_user: deps.CurrentUser,
        service: deps.Service
) -> models.UserBase:
    """Update current user"""

    await service.user.db_repository.update(
        models.User(
            id=c_user.id,
            username=user.username,
            password=deps.pwd_context.hash(user.password),
        )
    )
    await service.session.commit()
    await service.session.refresh(c_user)
    return models.UserBase(**c_user.model_dump())
