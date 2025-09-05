import logging

from fastapi import APIRouter, FastAPI

from src.auth.router import auth_router
from src.authors.router import author_router
from src.base.middleware import GlobalExceptionMiddleware
from src.books.router import books_router
from src.logger import configure_logging
from src.settings import Settings

logger = logging.getLogger(__name__)

settings = Settings.load()
configure_logging()

app = FastAPI(
    title='Library Platform API',
    description=(
        'A comprehensive REST API for managing books and authors in a library system. '
        'This API provides endpoints for author registration, authentication, book management, '
        'and bulk import functionality. Built with FastAPI, SQLAlchemy, and PostgreSQL.'
    ),
    version='1.0.0',
    contact={
        'name': 'Serhii Kryvtsun',
        'url': 'https://github.com/pitrella',
    },
    license_info={
        'name': 'MIT License',
        'url': 'https://opensource.org/licenses/MIT',
    },
    servers=[
        {
            'url': 'http://localhost:8000',
            'description': 'Development server',
        },
    ],
    openapi_tags=[
        {
            'name': 'auth',
            'description': 'Authentication and authorization endpoints. '
            'Handles user login, token refresh, and logout operations.',
        },
        {
            'name': 'author',
            'description': 'Author management endpoints. '
            'Handles author registration and profile management.',
        },
        {
            'name': 'books',
            'description': 'Book management endpoints. '
            'Handles CRUD operations for books, filtering, and bulk import.',
        },
    ],
)
app.add_middleware(GlobalExceptionMiddleware)

main_api_router = APIRouter(prefix='/api/v1')
main_api_router.include_router(author_router)
main_api_router.include_router(auth_router)
main_api_router.include_router(books_router)

app.include_router(main_api_router)
