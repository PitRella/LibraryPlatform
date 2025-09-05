"""Base exceptions for the application."""

from fastapi import HTTPException


class BaseException(HTTPException):
    """Base exception for all application errors."""


class UnknownTableException(BaseException):
    """Raised when an unknown table is referenced."""

    def __init__(self, table_name: str) -> None:
        """Initialize the exception with the table name.

        Args:
            table_name (str): Name of the unknown table.

        """
        super().__init__(
            status_code=400,
            detail=f'Unknown table: {table_name}',
        )


class ColumnNotAllowedException(BaseException):
    """Raised when a column is not allowed for a table."""

    def __init__(self, column_name: str, table_name: str) -> None:
        """Initialize the exception with column and table names.

        Args:
            column_name (str): Name of the not allowed column.
            table_name (str): Name of the table.

        """
        super().__init__(
            status_code=400,
            detail=f"Column '{column_name}' not allowed for table '{table_name}'",
        )


class OperatorNotAllowedException(BaseException):
    """Raised when an operator is not allowed."""

    def __init__(self, operator: str) -> None:
        """Initialize the exception with the operator.

        Args:
            operator (str): The not allowed operator.

        """
        super().__init__(
            status_code=400,
            detail=f"Operator '{operator}' not allowed",
        )


class ParameterNotFoundException(BaseException):
    """Raised when a required parameter is not found."""

    def __init__(self, param_name: str) -> None:
        """Initialize the exception with the parameter name.

        Args:
            param_name (str): Name of the missing parameter.

        """
        super().__init__(
            status_code=400,
            detail=f"Parameter '{param_name}' not found in params",
        )


class NoFieldsForUpdateException(BaseException):
    """Raised when no fields are provided for update."""

    def __init__(self) -> None:
        """Initialize the exception with a predefined error message."""
        super().__init__(
            status_code=400,
            detail='No fields provided for update',
        )
