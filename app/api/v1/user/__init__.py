from fastapi import APIRouter

from . import (
    create,
    retreive,
    update,
    delete
)

router = APIRouter(prefix='/user', tags=['user'])
router.include_router(create.router)
# router.include_router(delete.router)
router.include_router(retreive.router)
# router.include_router(update.router)
