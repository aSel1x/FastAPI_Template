from fastapi import APIRouter, Depends

from app import models

from ... import depends

router = APIRouter()


@router.get('/')
async def get(user: models.UserBase = Depends(depends.get_current_user)) -> models.UserBase:
    """
    Получить информацию о пользователе:

    - **id**: ID-пользователя
    - **username**: Username-Пользователя
    """
    return models.UserBase(**user.__dict__)
