from fastapi import APIRouter, Depends, HTTPException, status

from app import models
from app.service import Service

from ... import depends

router = APIRouter()


@router.post('/')
async def new_user(
    user: models.UserCreate, db: Service = Depends(depends.get_service)
) -> models.UserBase:
    """
    Создать нового пользователя:

    - **id**: ID-пользователя
    - **username**: Username-Пользователя
    - **password**: Password-Пользователя
    """

    if await db.user.db_repository.get_by_username(user.username):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='Такой пользователь существует.',
        )

    user = await db.user.db_repository.new(user)
    await db.session.commit()
    return models.UserBase(**user.__dict__)
