from sqlmodel import Field, SQLModel


class TokenAuth(SQLModel):
    token_auth: str = Field(
        'token_auth',
        title='Токен авторизации',
        description='Действует 15мин. необходим для получения пары токенов.',
    )


class TokenPair(SQLModel):
    token_long: str = Field(
        'token_long',
        title='Длинный токен',
        description='Действует  1год., необходим для получения нового короткого токена.',
    )
    token_short: str = Field(
        'token_short',
        title='Короткий токен',
        description='Действует 2часа., необходим для запросов к API',
    )
