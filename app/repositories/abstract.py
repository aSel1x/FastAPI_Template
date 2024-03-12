from abc import abstractmethod
from typing import Generic, Sequence, TypeVar

import sqlmodel as sm
from sqlalchemy import Result
from sqlmodel.ext.asyncio.session import AsyncSession

from ..models import BaseID

AbstractModel = TypeVar('AbstractModel', bound=BaseID)


class Repository(Generic[AbstractModel]):
    def __init__(self, type_model: type[BaseID], session: AsyncSession):
        self.type_model = type_model
        self.session = session

    async def get(
        self, ident: int | None = None, where_clauses: list[sm.DefaultClause] | None = None
    ) -> AbstractModel | None:
        if where_clauses is None and ident is not None:
            where_clauses = [self.type_model.id == ident]
        statement = sm.select(self.type_model).where(sm.and_(*where_clauses))
        return (await self.session.exec(statement)).one_or_none()

    async def get_many(
        self,
        where_clauses: list[sm.DefaultClause] | None = None,
        limit: int | None = None,
        order_by: sm.Column | None = None,
    ) -> Sequence[AbstractModel]:
        statement = sm.select(self.type_model).limit(limit).order_by(order_by)
        if where_clauses:
            statement = statement.where(sm.and_(*where_clauses))
        return (await self.session.exec(statement)).all()

    async def delete(
            self, ident: int | None = None, where_clauses: list[sm.DefaultClause] | None = None
    ) -> None:
        if where_clauses is None and ident is not None:
            where_clauses = [self.type_model.id == ident]
        statement = sm.delete(self.type_model).where(sm.and_(*where_clauses))
        await self.session.execute(statement)

    async def update(
        self, ident: int | None = None, where_clauses: list[sm.DefaultClause] | None = None, **values
    ) -> Result:
        if where_clauses is None and ident is not None:
            where_clauses = [self.type_model.id == ident]
        statement = (
            sm.update(self.type_model).values(**values).where(sm.and_(*where_clauses))
        )
        return await self.session.execute(statement)

    @abstractmethod
    async def new(self, in_model: AbstractModel) -> AbstractModel:
        ...
