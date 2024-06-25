from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app import api
from .core import settings

app = FastAPI(
    title=settings.APP_TITLE,
    root_path=settings.APP_PATH,
    version=settings.APP_VERSION,
    description=settings.app_description,
    contact={
        'name': 'aSel1x',
        'url': 'https://t.me/aSel1x',
        'email': 'asel1x@icloud.com',
    },
)


@app.exception_handler(Exception)
async def internal_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content=exc.__str__(),
    )

app.include_router(api.router)
