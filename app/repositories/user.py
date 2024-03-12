from sqlmodel.ext.asyncio.session import AsyncSession

from .. import models
from .abstract import Repository


class UserRepository(Repository[models.User]):

    def __init__(self, session: AsyncSession):
        super().__init__(type_model=models.User, session=session)

    async def new(self, in_model: models.UserBase) -> models.User:
        model = models.User(**in_model.model_dump())

        new_entry = await self.session.merge(model)
        await self.session.flush()
        return new_entry

    async def get_by_username(self, username: str, password: str | None = None) -> models.User | None:
        where_clauses = [
            self.type_model.username == username,
            (not password or self.type_model.password == password)
        ]
        entry = await self.get(where_clauses=where_clauses)
        return entry
