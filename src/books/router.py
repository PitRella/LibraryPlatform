from typing import Annotated, Any

from fastapi import APIRouter, Depends, File, Path, Query, UploadFile

from src.auth.dependencies import get_author_from_token
from src.base.dependencies import get_service
from src.books.responses import (
    CREATE_BOOK_RESPONSES,
    DELETE_BOOK_RESPONSES,
    GET_BOOK_RESPONSES,
    GET_BOOKS_RESPONSES,
    IMPORT_BOOKS_RESPONSES,
    UPDATE_BOOK_RESPONSES,
)
from src.books.schemas import (
    BookFiltersSchema,
    BookListParamsSchema,
    CreateBookRequestSchema,
    CreateBookResponseSchema,
    GetBookResponseSchema,
    GetBooksListResponseSchema,
    UpdateBookRequestSchema,
    UploadedBooksResponseSchema,
)
from src.books.services import BooksService

books_router = APIRouter(prefix='/books', tags=['books'])


@books_router.get(
    '/all',
    summary='Get all books',
    description='Retrieve all books with optional filters and pagination.',
    responses=GET_BOOKS_RESPONSES,
)
async def get_all_books(
    service: Annotated[BooksService, Depends(get_service(BooksService))],
    filters: Annotated[BookFiltersSchema, Depends()],
    limit: int = Query(10, gt=0, le=100, description='Maximum number of books'),
    cursor: int | None = Query(None, description='Cursor for pagination'),
) -> GetBooksListResponseSchema:
    """Retrieve all books matching given filters with pagination.

    Args:
        service (BooksService): Service dependency for book operations.
        limit (int): Max number of books to return.
        cursor (int | None): Pagination cursor.
        filters (BookFiltersSchema): Filters for books.

    Returns:
        GetBooksListResponseSchema: List of books and next cursor.

    """
    params = BookListParamsSchema(
        limit=limit,
        cursor=cursor,
        filters=filters,
    )
    books_result = await service.get_all_books(params)
    return GetBooksListResponseSchema(
        items=[
            GetBookResponseSchema.model_validate(b) for b in books_result.items
        ],
        next_cursor=books_result.next_cursor,
    )


@books_router.post(
    '/',
    summary='Create a new book',
    description='Create a new book by the authenticated author.',
    status_code=201,
    responses=CREATE_BOOK_RESPONSES,
)
async def create_book(
    author: Annotated[dict[str, Any], Depends(get_author_from_token)],
    book_schema: CreateBookRequestSchema,
    service: Annotated[BooksService, Depends(get_service(BooksService))],
) -> CreateBookResponseSchema:
    """Create a new book in the system.

    Args:
        author (dict[str, Any]): Authenticated author creating the book.
        book_schema (CreateBookRequestSchema): Book data.
        service (BooksService): Service dependency for book operations.

    Returns:
        CreateBookResponseSchema: ID of the created book.

    """
    book_id: int = await service.create_book(author, book_schema)
    return CreateBookResponseSchema(id=book_id)


@books_router.get(
    '/{book_id}',
    summary='Get a book',
    description='Retrieve details of a book by its ID.',
    responses=GET_BOOK_RESPONSES,
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
    """Retrieve a single book by ID.

    Args:
        service (BooksService): Service dependency for book operations.
        book_id (int): ID of the book to retrieve.

    Returns:
        GetBookResponseSchema: Book details.

    """
    book_data = await service.get_book(book_id)
    return GetBookResponseSchema.model_validate(book_data)


@books_router.patch(
    '/{book_id}',
    summary='Update a book',
    description='Update details of a book by its author.',
    responses=UPDATE_BOOK_RESPONSES,
)
async def update_book(
    author: Annotated[dict[str, Any], Depends(get_author_from_token)],
    update_book_schema: UpdateBookRequestSchema,
    service: Annotated[BooksService, Depends(get_service(BooksService))],
    book_id: int = Path(
        ...,
        ge=1,
        description='Book ID',
        examples=[1, 2, 3],
    ),
) -> GetBookResponseSchema:
    """Update book fields by author.

    Args:
        author (dict[str, Any]): Authenticated author performing update.
        update_book_schema (UpdateBookRequestSchema): Fields to update.
        service (BooksService): Service dependency for book operations.
        book_id (int): ID of the book to update.

    Returns:
        GetBookResponseSchema: Updated book details.

    """
    updated_book = await service.update_book(
        author=author, book_id=book_id, update_book_schema=update_book_schema
    )
    return GetBookResponseSchema.model_validate(updated_book)


@books_router.delete(
    '/{book_id}',
    summary='Delete a book',
    description='Delete a book by its author.',
    status_code=204,
    responses=DELETE_BOOK_RESPONSES,
)
async def delete_book(
    author: Annotated[dict[str, Any], Depends(get_author_from_token)],
    service: Annotated[BooksService, Depends(get_service(BooksService))],
    book_id: int = Path(..., ge=1, description='Book ID'),
) -> None:
    """Delete a book if author has permission.

    Args:
        author (dict[str, Any]): Authenticated author performing deletion.
        service (BooksService): Service dependency for book operations.
        book_id (int): ID of the book to delete.

    """
    await service.delete_book(
        author=author,
        book_id=book_id,
    )


@books_router.post(
    '/import',
    summary='Bulk import books',
    description='Upload a JSON or CSV file with books and import them.',
    status_code=201,
    responses=IMPORT_BOOKS_RESPONSES,
)
async def import_books(
    author: Annotated[dict[str, Any], Depends(get_author_from_token)],
    service: Annotated[BooksService, Depends(get_service(BooksService))],
    file: Annotated[UploadFile, File(description='Books file (JSON or CSV)')],
) -> UploadedBooksResponseSchema:
    """Import multiple books from a file.

    Args:
        author (dict[str, Any]): Authenticated author performing import.
        service (BooksService): Service dependency for book operations.
        file (UploadFile): JSON or CSV file containing books data.

    Returns:
        UploadedBooksResponseSchema: Number of books imported and their IDs.

    """
    books_info = await service.import_books(author, file)
    return UploadedBooksResponseSchema.model_validate(books_info.to_dict())
