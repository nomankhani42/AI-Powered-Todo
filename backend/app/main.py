"""FastAPI application factory and setup.

Initializes the FastAPI application with middleware, exception handlers,
and route registration.
"""

# Load environment variables from .env file FIRST
from dotenv import load_dotenv
import os
load_dotenv()

from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
import logging

from app.config import settings
from app.utils.logger import setup_logging
from app.utils.exceptions import AppException
from app.utils.response import create_error_response
from app.database.session import check_db_connection, init_db
from agents import set_tracing_disabled
from app.agents.openrouter_client import setup_openrouter_client

# Setup OpenAI Agents SDK to use OpenRouter's OpenAI-compatible endpoint
# This uses OpenRouter's native OpenAI compatibility with Qwen models
setup_openrouter_client()

# Disable tracing since we're using OpenRouter (not OpenAI)
# This prevents the SDK from trying to export traces to OpenAI backend
set_tracing_disabled(disabled=True)

# Setup logging
logger = setup_logging(__name__)

# Create FastAPI appr
app = FastAPI(
    title=settings.app_name,
    description=settings.app_description,
    version=settings.app_version,
    debug=settings.debug,
)

# CORS Middleware - Must be added FIRST (before other middleware)
# This ensures CORS headers are set for all requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
    allow_headers=["*"],
    expose_headers=["*"],
    max_age=3600,
)

# Log CORS configuration
logger.info(f"CORS enabled for origins: {settings.allowed_origins}")


# OPTIONS Handler for CORS Preflight
@app.options("/{full_path:path}")
async def preflight_handler(full_path: str):
    """Handle CORS preflight requests."""
    return {"status": "ok"}


# Exception Handlers
@app.exception_handler(AppException)
async def app_exception_handler(request: Request, exc: AppException):
    """Handle custom application exceptions."""
    logger.error(f"AppException: {exc.code} - {exc.message}")
    return create_error_response(
        code=exc.code,
        message=exc.message,
        status_code=exc.status_code,
        details=exc.details,
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Handle Pydantic validation errors."""
    logger.warning(f"Validation error: {exc.errors()}")
    return create_error_response( 
        code="VALIDATION_ERROR",
        message="Request validation failed",
        status_code=status.HTTP_400_BAD_REQUEST,
        details=exc.errors(),
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """Handle unexpected exceptions."""
    logger.exception(f"Unexpected error: {exc}")
    return create_error_response(
        code="INTERNAL_SERVER_ERROR",
        message="An unexpected error occurred",
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )


# Health Check Endpoint
@app.get("/health", tags=["Health"])
async def health_check():
    """Check application and database health.

    Returns:
        dict: Health status
    """
    db_ok = check_db_connection()
    return {
        "status": "healthy" if db_ok else "unhealthy",
        "database": "ok" if db_ok else "error",
    }


# API Route Registration
from app.api.auth import router as auth_router
from app.api.tasks import router as tasks_router
from app.api.agent import router as agent_router

app.include_router(auth_router, prefix="/api/v1/auth", tags=["Auth"])
app.include_router(tasks_router, prefix="/api/v1/tasks", tags=["Tasks"])
app.include_router(agent_router, prefix="/api/v1/agent", tags=["Agent"])

# API Documentation
@app.get("/docs", tags=["Documentation"], include_in_schema=False)
async def swagger_docs():
    """Swagger UI documentation."""
    return app.openapi()


@app.get("/redoc", tags=["Documentation"], include_in_schema=False)
async def redoc_docs():
    """ReDoc documentation."""
    return app.openapi()


# Startup Events
@app.on_event("startup")
async def startup_event():
    """Run on application startup."""
    logger.info(f"Starting {settings.app_name} (v{settings.app_version})")
    logger.info(f"Environment: {settings.environment}")
    logger.info(f"Debug mode: {settings.debug}")

    # Check database connection
    if check_db_connection():
        logger.info("Database connection OK")
        # Initialize database schema if it doesn't exist
        try:
            init_db()
            logger.info("Database schema initialized")
        except Exception as e:
            logger.warning(f"Failed to initialize database schema: {e}")
            logger.info("Continuing startup - tables may already exist")
    else:
        # In development, warn but don't crash if database unavailable
        if settings.is_development:
            logger.warning("Database connection failed - app running in degraded mode")
            logger.warning("To use database features, set DATABASE_URL to a valid Neon connection")
            logger.warning("Get started at: https://console.neon.tech")
        else:
            # In production, database is required
            logger.error("Failed to connect to database")
            raise RuntimeError("Database connection required in production environment")


@app.on_event("shutdown")
async def shutdown_event():
    """Run on application shutdown."""
    logger.info(f"Shutting down {settings.app_name}")


# Root endpoint
@app.get("/", tags=["Root"])
async def root():
    """API root endpoint.

    Returns:
        dict: API information
    """
    return {
        "name": settings.app_name,
        "version": settings.app_version,
        "docs": "/docs",
        "openapi": "/openapi.json",
    }
