from fastapi import APIRouter, Depends

from app import models

from ... import depends

router = APIRouter()


@router.get('/')
async def get(
        user: models.UserBase = Depends(depends.get_current_user)
) -> models.UserBase:
    """
    Get current user data:

    - **id**: ID
    - **username**: Username
    """
    return models.UserBase(**user.__dict__)
