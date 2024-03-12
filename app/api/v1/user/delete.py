from fastapi import APIRouter, Depends

from app import models
from app.service import Service

from ... import depends

router = APIRouter()


@router.delete('/')
async def delete_user(
        user: models.User = Depends(depends.get_current_user),
        service: Service = Depends(depends.get_service)
) -> None:

    await service.user.db_repository.delete(user.id)
    await service.session.commit()
