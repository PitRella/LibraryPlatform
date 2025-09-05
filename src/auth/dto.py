from dataclasses import dataclass
from datetime import datetime as dt

from src.base.dto import BaseDTO


@dataclass
class AccessTokenDTO(BaseDTO):
    """Data transfer object (DTO) for JWT access tokens.

    Attributes:
        sub (str): The subject (usually author/user ID) of the token.
        exp (datetime): The expiration datetime of the token.

    """

    sub: str
    exp: dt
