from pydantic import BaseModel, ConfigDict


class BaseSchema(BaseModel):
    """Base Pydantic schema for all request and response models.

    Provides a common configuration for Pydantic models, including
    `from_attributes=True` which allows parsing from arbitrary Python
    objects with attributes.

    Attributes:
        model_config (ConfigDict): Configuration for Pydantic model behavior.

    """

    model_config = ConfigDict(from_attributes=True)
