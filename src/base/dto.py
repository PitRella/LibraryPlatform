from dataclasses import asdict, dataclass
from typing import Any


@dataclass
class BaseDTO:
    """Base Data Transfer Object (DTO) class.

    Provides a helper method to convert the dataclass to a dictionary.
    All DTOs should inherit from this class.
    """

    def to_dict(self) -> dict[str, Any]:
        """Convert the DTO instance to a dictionary.

        Returns:
            dict[str, Any]: Dictionary representation of the DTO, where keys
            are field names and values are field values.

        """
        return asdict(self)
