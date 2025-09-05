import logging

from fastapi import APIRouter, FastAPI

from src.auth.router import auth_router
from src.logger import configure_logging
from src.settings import Settings
from src.authors.router import author_router
logger = logging.getLogger(__name__)

settings = Settings.load()
configure_logging()

app = FastAPI(title='LibraryPlatform')

main_api_router = APIRouter(prefix='/api/v1')
main_api_router.include_router(author_router)
main_api_router.include_router(auth_router)

app.include_router(main_api_router)

