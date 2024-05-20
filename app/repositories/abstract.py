import abc
from typing import Generic, Sequence, TypeVar

import sqlmodel as sm
from sqlmodel.ext.asyncio.session import AsyncSession

AbstractModel = TypeVar('AbstractModel', bound=sm.SQLModel)


class Repository(Generic[AbstractModel], metaclass=abc.ABCMeta):
    def __init__(self, model: type[AbstractModel], session: AsyncSession):
        self.model = model
        self.session = session

    async def create(self, model: AbstractModel) -> AbstractModel:
        self.model.model_validate(model)
        self.session.add(model)
        await self.session.commit()
        await self.session.refresh(model)
        return model

    async def retrieve_one(
            self,
            ident: int | None = None,
            where_clauses: list[sm.DefaultClause] | list[bool] | None = None,
    ) -> AbstractModel | None:
        if ident is not None:
            return await self.session.get(self.model, ident)
        stmt = sm.select(self.model).where(sm.and_(*where_clauses))
        entity = await self.session.exec(stmt)
        return entity.first()

    async def retrieve_many(
            self,
            where_clauses: list[sm.DefaultClause] | list[bool] | None = None,
    ) -> Sequence[AbstractModel] | None:
        stmt = sm.select(self.model).where(sm.and_(*where_clauses))
        entity = await self.session.exec(stmt)
        return entity.all()

    async def update(self, ident: int, **values) -> None:
        stmt = (
            sm.update(self.model)
            .where(self.model.id == ident)
            .values(values)
        )
        await self.session.execute(stmt)

    async def delete(
            self,
            ident: int | None = None,
            where_clauses: list[sm.DefaultClause] | None = None
    ) -> None:
        if ident is not None:
            where_clauses = [self.model.id == ident]
        stmt = sm.delete(self.model).where(sm.and_(*where_clauses))
        await self.session.execute(stmt)
