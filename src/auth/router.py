from typing import Annotated

from fastapi import APIRouter, Depends, Response

from fastapi.security import OAuth2PasswordRequestForm
from src.auth.schemas import TokenSchemas
from src.auth.services.auth import AuthService
from src.authors.models import Author
from src.base.dependencies import get_service

auth_router = APIRouter()


@auth_router.post(path='/login', response_model=TokenSchemas)
async def login_user(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    service: Annotated[AuthService, Depends(get_service(AuthService))],
    response: Response,
) -> TokenSchemas:
    author_data = await service.auth_user(
        email=form_data.username,
        password=form_data.password,
    )
