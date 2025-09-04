from fastapi import APIRouter

from src.authors.schemas import CreateAuthorRequestSchema

author_router = APIRouter(prefix='/author', tags=['author'])


@author_router.get('/', description='Create a new author.')
async def create_author(
        author_schema: CreateAuthorRequestSchema,
) -> None:
    pass
