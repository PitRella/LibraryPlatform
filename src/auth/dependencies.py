from typing import Annotated, Any

from fastapi import Depends
from fastapi.params import Security
from fastapi.security import OAuth2PasswordBearer

from src.auth.services import AuthService
from src.authors.service import AuthorService
from src.base.dependencies import get_service

oauth_scheme: OAuth2PasswordBearer = OAuth2PasswordBearer(
    tokenUrl='/auth/login',
)


async def get_author_from_token(
    token: Annotated[str, Security(oauth_scheme)],
    auth_service: Annotated[AuthService, Depends(get_service(AuthService))],
    author_service: Annotated[AuthorService, Depends(get_service(AuthorService))],
) -> dict[str, Any]:
    author_id = await auth_service.validate_token_for_user(token)
    return await author_service.get_author_by_id(author_id)