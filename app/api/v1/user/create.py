from fastapi import APIRouter, Depends, HTTPException, status

from app import models
from app.service import Service

from ... import depends

router = APIRouter()


@router.post('/')
async def new_user(
        user: models.UserCreate,
        service: Service = Depends(depends.get_service)
) -> models.UserBase:
    """
    Create new user:

    - **username**: Username
    - **password**: Password
    """

    if await service.user.db_repository.get_by_username(user.username):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='User exists.',
        )

    user = await service.user.db_repository.new(user)
    await service.session.commit()
    return models.UserBase(**user.__dict__)
