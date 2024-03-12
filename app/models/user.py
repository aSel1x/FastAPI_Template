from sqlmodel import SQLModel

from .base_id import BaseID


class UserBase(SQLModel):
    username: str
    is_active: bool = True


class UserCreate(UserBase):
    password: str


class User(UserBase, BaseID, table=True):  # type: ignore
    password: str
