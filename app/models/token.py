from sqlmodel import Field, SQLModel


class TokenAuth(SQLModel):
    token_auth: str = Field(
        'token_auth',
        title='Authorize token',
        description='Expires in 15 minutes. Needs to get pair token.',
    )


class TokenPair(SQLModel):
    token_long: str = Field(
        'token_long',
        title='Long token',
        description='Expires in year. Needs to get short token.',
    )
    token_short: str = Field(
        'token_short',
        title='Short token',
        description='Expires in 2 hours. Needs to get access to the API',
    )
