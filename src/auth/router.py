import uuid
from typing import Annotated, Any

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from src.auth.dependencies import get_author_from_token
from src.auth.schemas import RefreshTokenRequestSchema, TokenSchemas
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
) -> TokenSchemas:
    """Authenticate user and return access and refresh tokens.

    Args:
        form_data (OAuth2PasswordRequestForm): Username and password.
        service (AuthService): Auth service dependency.

    Returns:
        TokenSchemas: Access and refresh tokens with type.

    """
    author_data = await service.auth_user(
        email=form_data.username,
        password=form_data.password,
    )
    token: TokenSchemas = await service.create_token(author_data['id'])
    return token


@auth_router.get(path='/me')
async def get_me(
    author: Annotated[dict[str, Any] | None, Depends(get_author_from_token)],
) -> GetAuthorResponseSchema:
    """Retrieve the current authenticated author's profile.

    Args:
        author (dict[str, Any] | None): Author info from token dependency.

    Returns:
        GetAuthorResponseSchema: Current author details.

    """
    return GetAuthorResponseSchema.model_validate(author)


@auth_router.post(path='/refresh', response_model=TokenSchemas)
async def refresh_token(
    refresh_request: Annotated[RefreshTokenRequestSchema, Depends()],
    service: Annotated[AuthService, Depends(get_service(AuthService))],
) -> TokenSchemas:
    """Refresh access and refresh tokens using a valid refresh token.

    Args:
        refresh_request (RefreshTokenRequestSchema): Schema containing
            the refresh token.
        service (AuthService): Auth service dependency.

    Returns:
        TokenSchemas: New access and refresh tokens.

    """
    token: TokenSchemas = await service.refresh_token(
        refresh_token=uuid.UUID(refresh_request.refresh_token),
    )
    return token


@auth_router.delete(path='/logout', status_code=204)
async def logout_user(
    refresh_request: Annotated[RefreshTokenRequestSchema, Depends()],
    service: Annotated[AuthService, Depends(get_service(AuthService))],
) -> None:
    """Invalidate the provided refresh token, logging out the user.

    Args:
        refresh_request (RefreshTokenRequestSchema): Schema containing
            the refresh token to invalidate.
        service (AuthService): Auth service dependency.

    Returns:
        None

    """
    await service.logout_user(uuid.UUID(refresh_request.refresh_token))
