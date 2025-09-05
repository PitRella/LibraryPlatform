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
    description='API for managing books and authors',
    version='1.0.0',
    contact={'name': 'Serhii Kryvtsun', 'tg': '@pitrella'},
)
app.add_middleware(GlobalExceptionMiddleware)

main_api_router = APIRouter(prefix='/api/v1')
main_api_router.include_router(author_router)
main_api_router.include_router(auth_router)
main_api_router.include_router(books_router)

app.include_router(main_api_router)
