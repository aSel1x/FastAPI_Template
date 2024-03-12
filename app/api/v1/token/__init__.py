from fastapi import APIRouter

from . import auth, pair

router = APIRouter(prefix='/tokens', tags=['tokens'])
router.include_router(auth.router)
router.include_router(pair.router)
