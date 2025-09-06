from typing import Annotated, Any

from fastapi import Depends
from fastapi.params import Security
from fastapi.security import OAuth2PasswordBearer

from src.auth.services import AuthService
from src.authors.service import AuthorService
from src.base.dependencies import get_service

oauth_scheme: OAuth2PasswordBearer = OAuth2PasswordBearer(
    tokenUrl='/api/v1/auth/login',
)


async def get_author_from_token(
    token: Annotated[str, Security(oauth_scheme)],
    auth_service: Annotated[AuthService, Depends(get_service(AuthService))],
    author_service: Annotated[
        AuthorService, Depends(get_service(AuthorService))
    ],
) -> dict[str, Any]:
    """Retrieve the author information from a JWT access token.

    This dependency function validates the provided JWT access token, extracts
    the author ID, and fetches the full author record from the database.

    Args:
        token (str): JWT access token provided by the client.
        auth_service (AuthService): Service for validating JWT tokens.
        author_service (AuthorService): Service for fetching author data.

    Returns:
        dict[str, Any]: Dictionary containing the author's data.

    Raises:
        AuthorizationException: If the token is invalid or expired.
        AuthorNotFoundByIdException: If no author exists by ID.

    """
    author_id = await auth_service.validate_token_for_user(token)
    return await author_service.get_author_by_id(author_id)
