from datetime import datetime as dt
from typing import Annotated

from pydantic import Field, HttpUrl

from src.base.schemas import BaseSchema


class CreateAuthorRequestSchema(BaseSchema):
    name: Annotated[
        str, Field(
            min_length=4,
            max_length=16,
            pattern='^[a-zA-Z]+$',
            description="Author's name."
        )
    ]
    biography: Annotated[
        str | None, Field(
            min_length=16,
            max_length=256,
            pattern=r'^[a-zA-Z ]+$',
            description="Author's biography."
        )
    ]
    birth_year: Annotated[
        int | None,
        Field(
            ge=0,
            le=dt.now().year,
            description="Author's year of birth."
        )
    ]
    nationality: Annotated[
        str | None,
        Field(
            min_length=2,
            max_length=100,
            description="Nationality of the author."
        )
    ]
