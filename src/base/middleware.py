import logging
import uuid
from datetime import UTC, datetime

from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.types import ASGIApp

logger = logging.getLogger(__name__)


class GlobalExceptionMiddleware:
    def __init__(self, app: ASGIApp) -> None:
        self.app = app

    async def __call__(self, scope, receive, send) -> None:
        if scope['type'] != 'http':
            await self.app(scope, receive, send)
            return

        request = Request(scope, receive=receive)
        request_id = str(uuid.uuid4())
        scope.setdefault('state', {})
        scope['state']['request_id'] = request_id

        try:
            await self.app(scope, receive, send)
        except Exception as exc:
            if isinstance(exc, (HTTPException, StarletteHTTPException)):
                # Re-raise HTTP exceptions so they can be handled properly
                raise

            logger.exception('Unhandled exception (request_id=%s)', request_id)
            now = datetime.now(UTC).isoformat()
            response = JSONResponse(
                status_code=500,
                content={
                    'code': 'INTERNAL_SERVER_ERROR',
                    'message': 'An unexpected error occurred. Please try again later.',
                    'request_id': request_id,
                    'timestamp': now,
                },
            )
            await response(scope, receive, send)
