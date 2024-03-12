from fastapi import APIRouter, Depends

from app import models
from app.service import Service

from ... import depends

router = APIRouter()


@router.patch('/')
async def update_user(
        user: models.UserCreate,
        c_user: models.User = Depends(depends.get_current_user),
        service: Service = Depends(depends.get_service)
) -> None:
    """
    Update the current user:
    """

    await service.user.db_repository.update(ident=c_user.id, **user.model_dump())
    await service.session.commit()
