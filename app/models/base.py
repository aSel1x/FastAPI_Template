import datetime as dt
import uuid
from functools import partial

from sqlmodel import Column, Field, SQLModel

from app.core import types

datetime_utcnow = partial(dt.datetime.now, tz=dt.UTC)


class IDModel(SQLModel):
    id: int = Field(
        default=None,
        primary_key=True
    )


class UUIDModel(SQLModel):
    external_id: uuid.UUID = Field(
        default_factory=uuid.uuid4,
        unique=True
    )


class TimestampModel(SQLModel):
    created_at: dt.datetime = Field(default_factory=datetime_utcnow, sa_type=types.UnixepochType)
    updated_at: dt.datetime | None = Field(
        default_factory=datetime_utcnow,
        sa_column=Column(
            sa_type=types.UnixepochType,
            onupdate=datetime_utcnow
        )
    )
