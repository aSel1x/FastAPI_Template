import datetime as dt

from sqlalchemy.types import BigInteger, TypeDecorator


class UnixepochType(TypeDecorator):
    impl = BigInteger

    def load_dialect_impl(self, dialect):
        return dialect.type_descriptor(BigInteger())

    def process_bind_param(self, value: dt.datetime | dt.date, dialect) -> int | None:
        if isinstance(value, dt.datetime):
            return int(value.timestamp())
        elif isinstance(value, dt.date):
            return int(dt.datetime.combine(value, dt.time.min).timestamp())
        else:
            return None

    def process_result_value(self, value: int, dialect) -> dt.datetime:
        return dt.datetime.fromtimestamp(value, dt.UTC)
