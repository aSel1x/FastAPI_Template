from fastapi import BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession

from .services import UserService


class Service:

    def __init__(
            self,
            session: AsyncSession,
            background: BackgroundTasks,
    ):
        self.session = session
        self.background = background

        self.user = UserService(session, background)
