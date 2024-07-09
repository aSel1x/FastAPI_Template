from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncEngine, async_sessionmaker, create_async_engine
from sqlmodel.ext.asyncio.session import AsyncSession

from app import repositories as repos
from app.core import settings


def get_async_engine() -> AsyncEngine:
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


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with SessionLocal() as session:
        yield session


class Database:
    def __init__(self, session: AsyncSession):
        self.session = session

        self.user = repos.UserRepository(session)

    @classmethod
    async def get(cls) -> 'Database':
        async for session in get_session():
            return cls(session)
        raise RuntimeError('Unable to get database session')
