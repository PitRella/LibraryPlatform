from fastapi import HTTPException


class BookException(HTTPException):
    pass


class ForgottenParametersException(BookException):

    def __init__(self) -> None:
        super().__init__(
            status_code=400,
            detail='No fields provided for update',
        )
class BookNotFoundException(BookException):
    def __init__(self) -> None:
        super().__init__(
            status_code=404,
            detail='Book was not found',
        )
class BookPermissionException(BookException):
    def __init__(self) -> None:
        super().__init__(
            status_code=403,
            detail='Author book by id was not found',
        )


class ImportBadRequestException(BookException):
    def __init__(self, detail: str = 'Invalid import file') -> None:
        super().__init__(status_code=400, detail=detail)


class ImportUnsupportedFormatException(ImportBadRequestException):
    def __init__(self) -> None:
        super().__init__('Unsupported file format. Use .json or .csv')


class ImportMissingFilenameException(ImportBadRequestException):
    def __init__(self) -> None:
        super().__init__('File must have a filename')


class ImportInvalidJSONStructureException(ImportBadRequestException):
    def __init__(self) -> None:
        super().__init__('JSON must contain an array of books')


class ImportInvalidCSVStructureException(ImportBadRequestException):
    def __init__(self) -> None:
        super().__init__('Invalid CSV format')


class ImportItemValidationException(ImportBadRequestException):
    def __init__(self, detail: str = 'Invalid book data in imported file') -> None:
        super().__init__(detail)