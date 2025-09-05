import logging
import uuid
from datetime import UTC, datetime

from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.types import ASGIApp, Receive, Scope, Send

logger = logging.getLogger(__name__)


class GlobalExceptionMiddleware:
    """ASGI middleware for handling uncaught exceptions globally in FastAPI.

    This middleware intercepts all HTTP requests, generates a unique
    request ID for tracking, and ensures that unhandled exceptions are
    logged and returned as standardized JSON responses with a 500 status.

    Attributes:
        app (ASGIApp): The ASGI application to wrap.

    """

    def __init__(self, app: ASGIApp) -> None:
        """Initialize the middleware with the ASGI application.

        Args:
            app (ASGIApp): The ASGI application instance to wrap.

        """
        self.app: ASGIApp = app

    async def __call__(
        self, scope: Scope, receive: Receive, send: Send
    ) -> None:
        """Handle incoming requests and catch unhandled exceptions.

        Args:
            scope (Scope): ASGI connection scope containing request info.
            receive (Receive): ASGI receive callable for incoming events.
            send (Send): ASGI send callable for sending events.

        Raises:
            HTTPException: Re-raises FastAPI/Starlette HTTP exceptions to be
                handled by default handlers.

        Behavior:
            - Generates a unique request ID for each request.
            - Logs unexpected exceptions with request ID.
            - Returns a JSON response with status 500 for unhandled exceptions,
              including a timestamp and the request ID.

        """
        if scope['type'] != 'http':
            await self.app(scope, receive, send)
            return

        Request(scope, receive=receive)
        request_id: str = str(uuid.uuid4())
        scope.setdefault('state', {})
        scope['state']['request_id'] = request_id

        try:
            await self.app(scope, receive, send)
        except Exception as exc:
            if isinstance(exc, HTTPException | StarletteHTTPException):
                # Re-raise HTTP exceptions so they can be handled properly
                raise

            logger.exception('Unhandled exception (request_id=%s)', request_id)
            now: str = datetime.now(UTC).isoformat()
            response: JSONResponse = JSONResponse(
                status_code=500,
                content={
                    'code': 'INTERNAL_SERVER_ERROR',
                    'message': 'An unexpected error occurred. '
                    'Please try again later.',
                    'request_id': request_id,
                    'timestamp': now,
                },
            )
            await response(scope, receive, send)
