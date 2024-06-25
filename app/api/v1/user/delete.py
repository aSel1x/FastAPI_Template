from fastapi import APIRouter

from app import models
from app.api import deps

router = APIRouter()


@router.delete('/')
async def user_delete(
        user: deps.CurrentUser,
        service: deps.Service
) -> models.UserBase:
    """Mark user as inactive"""

    user.is_active = False
    await service.session.commit()
    return models.UserBase(**user.model_dump())
