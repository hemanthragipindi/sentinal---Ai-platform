from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from contextlib import asynccontextmanager

from app.core.config import settings
from app.core.logging import setup_logging, logger
from app.core.exceptions import (
    SentinelException, 
    sentinel_exception_handler, 
    http_exception_handler,
    validation_exception_handler,
    unhandled_exception_handler
)
from app.router import api_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup logic
    setup_logging()
    logger.info("Sentinel AI Security Platform starting up...")
    yield
    # Shutdown logic
    logger.info("Sentinel AI Security Platform shutting down...")

def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.PROJECT_NAME,
        version=settings.VERSION,
        openapi_url=f"{settings.API_V1_STR}/openapi.json",
        lifespan=lifespan
    )

    # CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.BACKEND_CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Exception Handlers
    app.add_exception_handler(SentinelException, sentinel_exception_handler)
    app.add_exception_handler(StarletteHTTPException, http_exception_handler)
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
    app.add_exception_handler(Exception, unhandled_exception_handler)

    # Router
    app.include_router(api_router, prefix=settings.API_V1_STR)

    return app

app = create_app()
