from fastapi import APIRouter

from app import models
from app.api import deps

router = APIRouter()


@router.get('/', response_model=models.UserBase)
async def user_retrieve(
        user: deps.CurrentUser
) -> models.UserBase:
    """Get current user"""

    return models.UserBase(**user.model_dump())
