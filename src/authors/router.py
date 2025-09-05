from typing import Annotated

from fastapi import APIRouter, Depends

from src.authors.schemas import CreateAuthorRequestSchema, \
    CreateAuthorResponseSchema
from src.authors.service import AuthorService
from src.base.dependencies import get_service

author_router = APIRouter(prefix='/author', tags=['author'])


@author_router.post('/', description='Create a new author.')
async def create_author(
        author_schema: CreateAuthorRequestSchema,
        service: Annotated[AuthorService, Depends(get_service(AuthorService))],
) -> CreateAuthorResponseSchema:
    author_id = await service.create_author(author_schema)
    return CreateAuthorResponseSchema(id=author_id)