from dataclasses import dataclass, asdict
from typing import Any



@dataclass
class BaseDTO:

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)