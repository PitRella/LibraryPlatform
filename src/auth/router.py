from typing import Annotated

from fastapi import APIRouter, Depends, Request, Response
from fastapi.security import OAuth2PasswordRequestForm

from src.auth.schemas import TokenSchemas
from src.auth.services.auth import AuthService
from src.base.dependencies import get_service
from src.settings import Settings

auth_router = APIRouter()
settings = Settings.load()


@auth_router.post(path='/login', response_model=TokenSchemas)
async def login_user(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    service: Annotated[AuthService, Depends(get_service(AuthService))],
    response: Response,
) -> TokenSchemas:
    pass
