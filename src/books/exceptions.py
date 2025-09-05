from fastapi import HTTPException


class BookException(HTTPException):
    """Base exception for book-related errors.

    Inherits from FastAPI HTTPException.
    All book-related exceptions should extend this class.
    """


class ForgottenParametersException(BookException):
    """Raised when no fields are provided for updating a book.

    Attributes:
        status_code (int): HTTP status code 422 (Unprocessable Entity).
        detail (str): Description of the error.

    """

    def __init__(self) -> None:
        """Initialize the exception with HTTP status and detail."""
        super().__init__(
            status_code=422,
            detail='No fields provided for update',
        )


class BookNotFoundException(BookException):
    """Raised when a book with the given ID does not exist.

    Attributes:
        status_code (int): HTTP status code 404 (Not Found).
        detail (str): Description of the error.

    """

    def __init__(self) -> None:
        """Initialize the exception with HTTP status and detail."""
        super().__init__(
            status_code=404,
            detail='Book was not found',
        )


class BookPermissionException(BookException):
    """Raised when the author is not allowed to access or modify the book.

    Attributes:
        status_code (int): HTTP status code 403 (Forbidden).
        detail (str): Description of the error.

    """

    def __init__(self) -> None:
        """Initialize the exception with HTTP status and detail."""
        super().__init__(
            status_code=403,
            detail='Author does not have permission to modify this book',
        )


class ImportBadRequestException(BookException):
    """Base exception for import-related errors.

    Attributes:
        status_code (int): HTTP status code 400 (Bad Request).
        detail (str): Description of the error.

    """

    def __init__(self, detail: str = 'Invalid import file') -> None:
        """Initialize the exception with HTTP status and detail.

        Args:
            detail (str): Error message describing the import problem.

        """
        super().__init__(status_code=400, detail=detail)


class ImportUnsupportedFormatException(ImportBadRequestException):
    """Raised when the uploaded import file format is not supported.

    Only .json and .csv formats are allowed.
    """

    def __init__(self) -> None:
        """Initialize the exception with a predefined error message."""
        super().__init__('Unsupported file format. Use .json or .csv')


class ImportMissingFilenameException(ImportBadRequestException):
    """Raised when the uploaded file has no filename."""

    def __init__(self) -> None:
        """Initialize the exception with a predefined error message."""
        super().__init__('File must have a filename')


class ImportInvalidJSONStructureException(ImportBadRequestException):
    """Raised when the uploaded JSON file does not contain an array of books."""

    def __init__(self) -> None:
        """Initialize the exception with a predefined error message."""
        super().__init__('JSON must contain an array of books')


class ImportInvalidCSVStructureException(ImportBadRequestException):
    """Raised when the uploaded CSV file structure is invalid."""

    def __init__(self) -> None:
        """Initialize the exception with a predefined error message."""
        super().__init__('Invalid CSV format')


class ImportItemValidationException(ImportBadRequestException):
    """Raised when an individual item in the imported file has invalid data.

    Attributes:
        detail (str): Description of the validation error for the item.

    """

    def __init__(
        self, detail: str = 'Invalid book data in imported file'
    ) -> None:
        """Initialize the exception with a detail message.

        Args:
            detail (str): Description of the invalid item data.

        """
        super().__init__(detail)


class NoUpdateDataException(BookException):
    """Raised when no update data is provided."""

    def __init__(self) -> None:
        """Initialize the exception with a predefined error message."""
        super().__init__(
            status_code=400,
            detail='No update data provided',
        )


class NoFiltersException(BookException):
    """Raised when no filters are provided for an operation."""

    def __init__(self) -> None:
        """Initialize the exception with a predefined error message."""
        super().__init__(
            status_code=400,
            detail='No filters provided for operation',
        )


class UnsafeFilterException(BookException):
    """Raised when an unsafe filter is detected."""

    def __init__(self, filter_str: str) -> None:
        """Initialize the exception with the unsafe filter string.

        Args:
            filter_str (str): The unsafe filter string that was detected.

        """
        super().__init__(
            status_code=400,
            detail=f'Unsafe filter detected: {filter_str}',
        )
