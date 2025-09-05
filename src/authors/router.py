from typing import Annotated

from fastapi import APIRouter, Depends

from src.authors.responses import CREATE_AUTHOR_RESPONSES
from src.authors.schemas import (
    CreateAuthorRequestSchema,
    CreateAuthorResponseSchema,
)
from src.authors.service import AuthorService
from src.base.dependencies import get_service

author_router = APIRouter(prefix='/author', tags=['author'])


@author_router.post(
    '/',
    summary='Create a new author',
    description=(
        'Create a new author account with email, password, and profile info.'
    ),
    status_code=201,
    responses=CREATE_AUTHOR_RESPONSES,
)
async def create_author(
    author_schema: CreateAuthorRequestSchema,
    service: Annotated[AuthorService, Depends(get_service(AuthorService))],
) -> CreateAuthorResponseSchema:
    """Create a new author in the system.

    This endpoint accepts author details such as email, password, and name,
    validates them, and creates a new author record.

    Args:
        author_schema (CreateAuthorRequestSchema): Request schema containing
            the details of the author to be created.
        service (AuthorService): Service instance injected by dependency
            injection to handle business logic.

    Returns:
        CreateAuthorResponseSchema: Response schema containing the ID
        of the newly created author.

    """
    author_id = await service.create_author(author_schema)
    return CreateAuthorResponseSchema(id=author_id)
