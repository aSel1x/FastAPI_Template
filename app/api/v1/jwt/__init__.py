from fastapi import APIRouter

from . import auth

router = APIRouter(prefix='/token', tags=['token'])
router.include_router(auth.router)
