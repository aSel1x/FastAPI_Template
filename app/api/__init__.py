from fastapi import APIRouter, Depends

from . import (
    v1,
)

router = APIRouter()
router.include_router(v1.router)
