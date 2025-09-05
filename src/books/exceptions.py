from fastapi import HTTPException


class BookException(HTTPException):
    """Base exception for book-related errors."""


class ForgottenParametersException(BookException):
    """Raised when no fields are provided for update."""
    def __init__(self) -> None:
        super().__init__(
            status_code=422,
            detail='No fields provided for update',
        )


class BookNotFoundException(BookException):
    """Raised when a book with the given ID is not found."""
    def __init__(self) -> None:
        super().__init__(
            status_code=404,
            detail='Book was not found',
        )


class BookPermissionException(BookException):
    """Raised when the author is not allowed to access or modify the book."""
    def __init__(self) -> None:
        super().__init__(
            status_code=403,
            detail='Author does not have permission to modify this book',
        )


class ImportBadRequestException(BookException):
    """Base exception for import-related errors."""
    def __init__(self, detail: str = 'Invalid import file') -> None:
        super().__init__(status_code=400, detail=detail)


class ImportUnsupportedFormatException(ImportBadRequestException):
    """Raised when import file format is not supported."""
    def __init__(self) -> None:
        super().__init__('Unsupported file format. Use .json or .csv')


class ImportMissingFilenameException(ImportBadRequestException):
    """Raised when the uploaded file has no filename."""
    def __init__(self) -> None:
        super().__init__('File must have a filename')


class ImportInvalidJSONStructureException(ImportBadRequestException):
    """Raised when JSON file does not contain an array of books."""
    def __init__(self) -> None:
        super().__init__('JSON must contain an array of books')


class ImportInvalidCSVStructureException(ImportBadRequestException):
    """Raised when CSV file structure is invalid."""
    def __init__(self) -> None:
        super().__init__('Invalid CSV format')


class ImportItemValidationException(ImportBadRequestException):
    """Raised when an individual item in the import file is invalid."""
    def __init__(
        self, detail: str = 'Invalid book data in imported file'
    ) -> None:
        super().__init__(detail)
