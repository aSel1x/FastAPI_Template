from sqlmodel import Field, SQLModel

from .base import IDModel, TimestampModel


class UserBase(SQLModel):
    username: str = Field()
    is_active: bool = Field(default=True)


class UserCreate(SQLModel):
    username: str = Field()
    password: str = Field()


class User(UserBase, IDModel, TimestampModel, table=True):  # type: ignore
    password: str = Field()
