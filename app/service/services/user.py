from fastapi import BackgroundTasks
from sqlmodel.ext.asyncio.session import AsyncSession

from app import models, repositories


class UserService:

    def __init__(
            self,
            session: AsyncSession,
            background: BackgroundTasks
    ):
        self.type_model = models.User
        self.session = session
        self.background = background
        self.db_repository = repositories.UserRepository(session)
