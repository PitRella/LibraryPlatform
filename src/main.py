import logging

from fastapi import APIRouter, FastAPI

from src.logger import configure_logging
from src.settings import Settings

logger = logging.getLogger(__name__)

settings = Settings.load()
configure_logging()

app = FastAPI(title='LibraryPlatform')

main_api_router = APIRouter(prefix='/api/v1')

app.include_router(main_api_router)

