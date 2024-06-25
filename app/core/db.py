from sqlalchemy.ext.asyncio import AsyncEngine, async_sessionmaker, create_async_engine
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core import settings


def get_async_engine() -> AsyncEngine:
    print(settings.pg_dsn)
    engine: AsyncEngine = create_async_engine(
        settings.pg_dsn.unicode_string(), echo=False, future=True
    )
    return engine


SessionLocal = async_sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=get_async_engine(),
    class_=AsyncSession,
    expire_on_commit=False,
)
