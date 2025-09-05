"""Response examples for books endpoints."""

# Common responses
UNAUTHORIZED_RESPONSE = {
    401: {
        'description': 'Unauthorized - Invalid or missing token',
        'content': {
            'application/json': {
                'example': {'detail': 'Could not validate credentials'}
            }
        }
    }
}

VALIDATION_ERROR_RESPONSE = {
    422: {
        'description': 'Validation Error',
        'content': {
            'application/json': {
                'example': {
                    'detail': [
                        {
                            'type': 'string_too_short',
                            'loc': ['body', 'title'],
                            'msg': 'String should have at least 2 characters',
                            'input': 'A',
                        }
                    ]
                }
            }
        }
    }
}

NOT_FOUND_RESPONSE = {
    404: {
        'description': 'Book not found',
        'content': {
            'application/json': {
                'example': {'detail': 'Book with ID 999 not found'}
            }
        }
    }
}

FORBIDDEN_RESPONSE = {
    403: {
        'description': 'Forbidden - Not the author of this book',
        'content': {
            'application/json': {
                'example': {'detail': 'You can only update your own books'}
            }
        }
    }
}

# Books specific responses
GET_BOOKS_RESPONSES = {
    200: {
        'description': 'Successfully retrieved books list',
        'content': {
            'application/json': {
                'example': {
                    'items': [
                        {
                            'id': 1,
                            'title': 'Romeo and Juliet',
                            'genre': 'FICTION',
                            'language': 'ENGLISH',
                            'published_year': 1597,
                        }
                    ],
                    'next_cursor': 2,
                }
            }
        }
    },
    400: {
        'description': 'Bad Request - Invalid parameters',
        'content': {
            'application/json': {
                'example': {'detail': 'Invalid filter parameters'}
            }
        }
    },
    **VALIDATION_ERROR_RESPONSE,
}

CREATE_BOOK_RESPONSES = {
    201: {
        'description': 'Book successfully created',
        'content': {'application/json': {'example': {'id': 1}}},
    },
    400: {
        'description': 'Bad Request - Invalid book data',
        'content': {
            'application/json': {
                'example': {'detail': 'Invalid book data provided'}
            }
        }
    },
    **UNAUTHORIZED_RESPONSE,
    **VALIDATION_ERROR_RESPONSE,
}

GET_BOOK_RESPONSES = {
    200: {
        'description': 'Book successfully retrieved',
        'content': {
            'application/json': {
                'example': {
                    'id': 1,
                    'title': 'Romeo and Juliet',
                    'genre': 'FICTION',
                    'language': 'ENGLISH',
                    'published_year': 1597,
                }
            }
        }
    },
    **NOT_FOUND_RESPONSE,
    **VALIDATION_ERROR_RESPONSE,
}

UPDATE_BOOK_RESPONSES = {
    200: {
        'description': 'Book successfully updated',
        'content': {
            'application/json': {
                'example': {
                    'id': 1,
                    'title': 'Updated Book Title',
                    'genre': 'NON_FICTION',
                    'language': 'ENGLISH',
                    'published_year': 2023,
                }
            }
        }
    },
    **UNAUTHORIZED_RESPONSE,
    **FORBIDDEN_RESPONSE,
    **NOT_FOUND_RESPONSE,
    **VALIDATION_ERROR_RESPONSE,
}

DELETE_BOOK_RESPONSES = {
    204: {'description': 'Book successfully deleted'},
    **UNAUTHORIZED_RESPONSE,
    **FORBIDDEN_RESPONSE,
    **NOT_FOUND_RESPONSE,
    **VALIDATION_ERROR_RESPONSE,
}

IMPORT_BOOKS_RESPONSES = {
    201: {
        'description': 'Books successfully imported',
        'content': {'application/json': {'example': {'imported': 5, 'book_ids': [1, 2, 3, 4, 5]}}},
    },
    400: {
        'description': 'Bad Request - Invalid file format or content',
        'content': {
            'application/json': {
                'example': {'detail': 'Invalid file format. Only JSON and CSV are supported.'}
            }
        }
    },
    **UNAUTHORIZED_RESPONSE,
    413: {
        'description': 'File too large',
        'content': {
            'application/json': {
                'example': {'detail': 'File size exceeds maximum allowed size of 10MB'}
            }
        }
    },
    **VALIDATION_ERROR_RESPONSE,
}