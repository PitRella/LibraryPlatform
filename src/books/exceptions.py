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