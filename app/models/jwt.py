from sqlmodel import Field, SQLModel


class AccessToken(SQLModel):
    token: str = Field(
        None, description='Необходим для запросов к API, действует 24 часа.'
    )
