from fastapi import FastAPI

from app import api
from .core import settings

app = FastAPI(
    title='FastAPI template',
    openapi_prefix=settings.API_PREFIX
)
app.include_router(api.router)
