import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, Response
from fastapi.requests import Request
from fastapi.security import OAuth2PasswordRequestForm
from src.auth.schemas import TokenSchemas
from src.auth.services.auth import AuthService
from src.base.dependencies import get_service
from src.settings import Settings

auth_router = APIRouter()
settings = Settings.load()


@auth_router.post(path='/login', response_model=TokenSchemas)
async def login_user(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    service: Annotated[AuthService, Depends(get_service(AuthService))],
    response: Response,
) -> TokenSchemas:
    author_data = await service.auth_user(
        email=form_data.username,
        password=form_data.password,
    )
    token: TokenSchemas = await service.create_token(author_data['id'])
    response.set_cookie(
        'access_token',
        token.access_token,
        max_age=settings.token_settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        httponly=True,
    )
    response.set_cookie(
        'refresh_token',
        token.refresh_token,
        max_age=settings.token_settings.REFRESH_TOKEN_EXPIRE_DAYS
                * 30
                * 24
                * 60,
        httponly=True,
    )
    return token


@auth_router.post(path='/refresh', response_model=TokenSchemas)
async def refresh_token(
    request: Request,
    response: Response,
    service: Annotated[AuthService, Depends(get_service(AuthService))],
) -> TokenSchemas:
    token: TokenSchemas = await service.refresh_token(
        refresh_token=uuid.UUID(request.cookies.get('refresh_token')),
    )
    response.set_cookie(
        'access_token',
        token.access_token,
        max_age=settings.token_settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        httponly=True,
    )
    response.set_cookie(
        'refresh_token',
        token.refresh_token,
        max_age=settings.token_settings.REFRESH_TOKEN_EXPIRE_DAYS
        * 30
        * 24
        * 60,
        httponly=True,
    )
    return token