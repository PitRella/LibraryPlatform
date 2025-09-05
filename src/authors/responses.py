"""Response examples for authors endpoints."""

# Common responses
VALIDATION_ERROR_RESPONSE = {
    422: {
        'description': 'Validation Error',
        'content': {
            'application/json': {
                'example': {
                    'detail': [
                        {
                            'type': 'string_too_short',
                            'loc': ['body', 'name'],
                            'msg': 'String should have at least 2 characters',
                            'input': 'A',
                        }
                    ]
                }
            }
        }
    }
}

# Authors specific responses
CREATE_AUTHOR_RESPONSES = {
    201: {
        'description': 'Author successfully created',
        'content': {'application/json': {'example': {'id': 1}}},
    },
    400: {
        'description': 'Bad Request - Invalid author data',
        'content': {
            'application/json': {
                'example': {'detail': 'Email already exists'}
            }
        }
    },
    **VALIDATION_ERROR_RESPONSE,
}