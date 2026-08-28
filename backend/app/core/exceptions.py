from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.shared.schemas import error_response
from app.core.logging import logger

class SentinelException(Exception):
    def __init__(self, message: str, status_code: int = 400, data: dict = None):
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.data = data

async def sentinel_exception_handler(request: Request, exc: SentinelException):
    logger.warning(f"SentinelException: {exc.message}")
    return JSONResponse(
        status_code=exc.status_code,
        content=error_response(message=exc.message, data=exc.data).model_dump(),
    )

async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    logger.warning(f"HTTPException: {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content=error_response(message=str(exc.detail)).model_dump(),
    )

async def validation_exception_handler(request: Request, exc: RequestValidationError):
    logger.warning(f"Validation Error: {exc.errors()}")
    return JSONResponse(
        status_code=422,
        content=error_response(message="Validation Error", data={"errors": exc.errors()}).model_dump(),
    )

async def unhandled_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled Exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content=error_response(message="An internal server error occurred.").model_dump(),
    )
