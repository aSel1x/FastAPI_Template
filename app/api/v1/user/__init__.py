from fastapi import APIRouter

from . import (
    auth,
    create,
    retreive,
    delete
)

router = APIRouter(prefix='/user', tags=['user'])
router.include_router(auth.router)
router.include_router(create.router)
router.include_router(delete.router)
router.include_router(retreive.router)
