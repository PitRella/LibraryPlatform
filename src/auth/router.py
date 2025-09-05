import uuid
from typing import Annotated, Any

from fastapi import APIRouter, Depends, Response
from fastapi.requests import Request
from fastapi.security import OAuth2PasswordRequestForm

from src.auth.dependencies import get_author_from_token
from src.auth.schemas import TokenSchemas
from src.auth.services.auth import AuthService
from src.authors.schemas import GetAuthorResponseSchema
from src.base.dependencies import get_service
from src.settings import Settings

auth_router = APIRouter(prefix='/auth', tags=['auth'])
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


@auth_router.get(path='/me')
async def get_me(
        author: Annotated[
            dict[str, Any] | None, Depends(get_author_from_token)
        ],
) -> GetAuthorResponseSchema:
    return GetAuthorResponseSchema.model_validate(author)


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


@auth_router.delete(path='/logout', status_code=204)
async def logout_user(
        request: Request,
        response: Response,
        service: Annotated[AuthService, Depends(get_service(AuthService))],
) -> None:
    await service.logout_user(request.cookies.get('refresh_token'))
    response.delete_cookie('access_token')
    response.delete_cookie('refresh_token')
    return None
