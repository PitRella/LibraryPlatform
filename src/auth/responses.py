"""Response examples for auth endpoints."""

from typing import Any

# Common responses
UNAUTHORIZED_RESPONSE: dict[int | str, dict[str, Any]] = {
    401: {
        'description': 'Unauthorized - Invalid or missing token',
        'content': {
            'application/json': {
                'example': {'detail': 'Could not validate credentials'}
            }
        },
    }
}

VALIDATION_ERROR_RESPONSE: dict[int | str, dict[str, Any]] = {
    422: {
        'description': 'Validation Error',
        'content': {
            'application/json': {
                'example': {
                    'detail': [
                        {
                            'type': 'missing',
                            'loc': ['body', 'username'],
                            'msg': 'Field required',
                            'input': None,
                        }
                    ]
                }
            }
        },
    }
}

# Auth specific responses
LOGIN_RESPONSES: dict[int | str, dict[str, Any]] = {
    200: {
        'description': 'Successfully authenticated',
        'content': {
            'application/json': {
                'example': {
                    'access_token': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...',
                    'refresh_token': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...',
                    'token_type': 'Bearer',
                }
            }
        },
    },
    401: {
        'description': 'Invalid credentials',
        'content': {
            'application/json': {
                'example': {'detail': 'Incorrect email or password'}
            }
        },
    },
    **VALIDATION_ERROR_RESPONSE,
}

GET_ME_RESPONSES: dict[int | str, dict[str, Any]] = {
    200: {
        'description': 'Successfully retrieved user profile',
        'content': {
            'application/json': {
                'example': {
                    'email': 'author@example.com',
                    'name': 'John Smith',
                    'biography': (
                        'I am a passionate writer who loves creating worlds.'
                    ),
                    'birth_year': 1985,
                    'nationality': 'United Kingdom',
                }
            }
        },
    },
    **UNAUTHORIZED_RESPONSE,
}

REFRESH_TOKEN_RESPONSES: dict[int | str, dict[str, Any]] = {
    200: {
        'description': 'Successfully refreshed tokens',
        'content': {
            'application/json': {
                'example': {
                    'access_token': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...',
                    'refresh_token': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...',
                    'token_type': 'Bearer',
                }
            }
        },
    },
    401: {
        'description': 'Invalid or expired refresh token',
        'content': {
            'application/json': {
                'example': {'detail': 'Invalid or expired refresh token'}
            }
        },
    },
    **VALIDATION_ERROR_RESPONSE,
}

LOGOUT_RESPONSES: dict[int | str, dict[str, Any]] = {
    204: {'description': 'Successfully logged out'},
    401: {
        'description': 'Invalid or expired refresh token',
        'content': {
            'application/json': {
                'example': {'detail': 'Invalid or expired refresh token'}
            }
        },
    },
    **VALIDATION_ERROR_RESPONSE,
}
