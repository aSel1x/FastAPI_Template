from fastapi import APIRouter, Depends, HTTPException, Response, status

from app import models
from app.core import security
from app.service import Service

from ... import depends

router = APIRouter()


@router.get('/pair/')
async def get_token_pair(
    response: Response,
    token: str,
    service: Service = Depends(depends.get_service),
) -> models.TokenPair:
    if not (data := security.decode_token(token)):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='The authorization token expired.',
        )
    if (payload := data.get('payload')) is None or not isinstance(payload, dict):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='This must be an authorization token or a long token',
        )

    if data.get('action') not in ['token_auth', 'token_long']:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='This must be an authorization token or a long token',
        )

    if await service.user.db_repository.retrieve_one(ident=payload.get('id')):
        token_pair = security.create_token_pair(payload)
        if data.get('action') != 'token_long':
            response.set_cookie(key='_token_long', value=token_pair.token_long)
            response.set_cookie(key='_token_short', value=token_pair.token_short)
        else:
            token_pair.token_long = token
            response.set_cookie(key='_token_short', value=token_pair.token_short)

        return token_pair
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail='User not found'
        )
