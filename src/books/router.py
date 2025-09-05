import csv
import json
from fastapi import HTTPException
from io import StringIO
from typing import Annotated, Any
from datetime import datetime as dt

from fastapi import Depends, Query, APIRouter, Path, UploadFile, File
from src.auth.dependencies import get_author_from_token
from src.base.dependencies import get_service
from src.books.enum import BookGenre, BookLanguage
from src.books.schemas import CreateBookRequestSchema, GetBookResponseSchema, \
    UpdateBookRequestSchema, CreateBookResponseSchema
from src.books.service import BooksService

books_router = APIRouter(prefix='/books', tags=['books'])


@books_router.get(
    '/all',
    summary='Get all books',
    description='Retrieve all books by filters'
)
async def get_all_books(
        service: Annotated[BooksService, Depends(get_service(BooksService))],
        limit: int = Query(10, gt=0, le=100, description='Limit of books'),
        cursor: int | None = Query(None, description='Cursor for pagination'),
        title: str | None = Query(
            None,
            min_length=1,
            max_length=50,
            pattern=r'^[a-zA-Z\s\-\'\.]+$',
            description='Book title',
            examples=["Romeo and Juliet", "The Shining"],
        ),
        genre: BookGenre | None = None,
        language: BookLanguage | None = None,
        published_year: int | None = Query(
            None,
            ge=1800,
            le=dt.now().year,
            description='Book published year',
            examples=[1985, 2022],
        ),
        author_id: int | None = Query(None, ge=0),
) -> list[GetBookResponseSchema] | None:
    books = await service.get_all_books(
        limit=limit,
        cursor=cursor,
        title=title,
        genre=genre,
        language=language,
        published_year=published_year,
        author_id=author_id,
    )
    return [GetBookResponseSchema.model_validate(b) for b in books]


@books_router.post(
    '/',
    summary='Create a new book.',
    description='Create a new book by author.'
)
async def create_book(
        author: Annotated[
            dict[str, Any], Depends(get_author_from_token)
        ],
        book_schema: CreateBookRequestSchema,
        service: Annotated[BooksService, Depends(get_service(BooksService))],
) -> CreateBookResponseSchema:
    book_id: int = await service.create_book(author, book_schema)
    return CreateBookResponseSchema(id=book_id)


@books_router.get(
    '/{book_id}',
    summary='Get a book.',
    description='Get a book published by author.',
)
async def get_book(
        service: Annotated[BooksService, Depends(get_service(BooksService))],
        book_id: int = Path(
            ...,
            ge=1,
            description='Book ID',
            examples=[1, 2, 3],
        ),
) -> GetBookResponseSchema:
    book_data = await service.get_book(book_id)
    return GetBookResponseSchema.model_validate(book_data)


@books_router.patch('/{book_id}', description='Change book parameters')
async def update_book(
        author: Annotated[
            dict[str, Any], Depends(get_author_from_token)
        ],
        update_book_schema: UpdateBookRequestSchema,
        service: Annotated[BooksService, Depends(get_service(BooksService))],
        book_id: int = Path(
            ...,
            ge=1,
            description='Book ID',
            examples=[1, 2, 3],
        ),
) -> GetBookResponseSchema:
    updated_book = await service.update_book(
        author=author,
        book_id=book_id,
        update_book_schema=update_book_schema
    )
    return GetBookResponseSchema.model_validate(updated_book)


@books_router.delete('/{book_id}', description='Delete book', status_code=204)
async def delete_book(
        author: Annotated[
            dict[str, Any], Depends(get_author_from_token)
        ],
        service: Annotated[BooksService, Depends(get_service(BooksService))],
        book_id: int = Path(..., ge=1, description='Book ID'),

) -> None:
    await service.delete_book(
        author=author,
        book_id=book_id,
    )
    return None


@books_router.post(
    "/import",
    summary="Bulk import books",
    description="Upload a JSON or CSV file with books and import them into the system.",
    status_code=201,
)
async def import_books(
        author: Annotated[dict[str, Any], Depends(get_author_from_token)],
        service: Annotated[BooksService, Depends(get_service(BooksService))],
        file: UploadFile = File(..., description="Books file (JSON or CSV)"),
) -> dict[str, Any]:
    content = await file.read()
    books_to_create = []
    try:
        if file.filename.endswith(".json"):
            data = json.loads(content.decode("utf-8"))
            if not isinstance(data, list):
                raise ValueError("JSON file must contain an array of books")
            books_to_create = data

        elif file.filename.endswith(".csv"):
            reader = csv.DictReader(StringIO(content.decode("utf-8")))
            books_to_create = list(reader)

        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Unsupported file format. Use .json or .csv"
            )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to parse file: {e}"
        )

    created_ids: list[int] = []
    for book in books_to_create:
        schema = CreateBookRequestSchema(**book)
        book_id = await service.create_book(author, schema)
        created_ids.append(book_id)

    return {
        "imported": len(created_ids),
        "book_ids": created_ids
    }
