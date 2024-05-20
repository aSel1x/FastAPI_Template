from sqlmodel.ext.asyncio.session import AsyncSession

from .. import models
from .abstract import Repository


class UserRepository(Repository[models.User]):
    def __init__(self, session: AsyncSession):
        super().__init__(model=models.User, session=session)

    async def new(self, in_model: models.UserBase) -> models.User:
        model = models.User(**in_model.model_dump())

        entry = await self.create(model)
        await self.session.flush()
        return entry

    async def get_by_username(self, username: str, password: str | None = None) -> models.User | None:
        where_clauses = [
            self.model.username == username,
            (not password or self.model.password == password)
        ]
        entry = await self.retrieve_one(where_clauses=where_clauses)
        return entry
