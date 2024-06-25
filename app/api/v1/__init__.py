from fastapi import APIRouter
from . import (
    user,
    jwt,
)

router = APIRouter(prefix='/v1')
router.include_router(user.router)
router.include_router(jwt.router)
