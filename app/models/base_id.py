from sqlalchemy.orm import declared_attr
from sqlmodel import Field, SQLModel


class BaseID(SQLModel):

    @classmethod
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    __allow_unmapped__ = False

    id: int | None = Field(default=None, primary_key=True)

    def __repr__(self):
        return f'{__class__.__name__}({self.id=})'
