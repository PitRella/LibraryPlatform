from dataclasses import dataclass
from datetime import datetime as dt

from src.base.dto import BaseDTO


@dataclass
class AccessTokenDTO(BaseDTO):
    sub: str
    exp: dt
