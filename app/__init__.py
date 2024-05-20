from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app import api
from .core import settings

app = FastAPI(
    title='FastAPI Template',
    openapi_prefix=settings.API_PREFIX
)


@app.exception_handler(Exception)
async def internal_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content=exc.__str__(),
    )

app.include_router(api.router)
