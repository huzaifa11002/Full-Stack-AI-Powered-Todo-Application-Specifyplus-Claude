"""FastAPI application entry point for Todo REST API.

This module configures:
- FastAPI application instance
- CORS middleware for frontend integration
- Task router with /api prefix
- Health check endpoints
- Startup/shutdown event handlers
"""

import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from sqlalchemy import text
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

from app.routers import tasks, auth, chat
from app.database import engine
from app.middleware.auth import JWTAuthMiddleware
from sqlmodel import Session


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager for startup and shutdown events."""
    # Startup: Verify database connection
    print("Starting up FastAPI Todo API...")
    try:
        print("DIAGNOSTIC: Backend starting up. Checking password module...")
        from app.utils import password
        print(f"DIAGNOSTIC: Password module file: {password.__file__}")
        with Session(engine) as session:
            # Test database connection
            session.exec(text("SELECT 1"))
            print("Database connection verified successfully!")
    except Exception as e:
        print(f"WARNING: Database connection failed: {e}")
        print("API will start but database operations may fail.")

    yield

    # Shutdown: Cleanup
    print("Shutting down FastAPI Todo API...")
    engine.dispose()
    print("Database connections closed.")


# Create FastAPI application instance
app = FastAPI(
    title="FastAPI Todo REST API",
    description="Multi-user todo application with user isolation",
    version="1.0.0",
    lifespan=lifespan
)

# Configure rate limiter
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Configure CORS middleware
# Support multiple origins for k8s/minikube deployment
FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:3000")
CORS_ORIGINS = os.getenv("CORS_ORIGINS", FRONTEND_URL)
# Parse comma-separated origins or use single URL
allowed_origins = [origin.strip() for origin in CORS_ORIGINS.split(",")] if CORS_ORIGINS else [FRONTEND_URL]

print(f"[CORS] Allowed origins: {allowed_origins}")

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,  # Support multiple origins
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE"],
    allow_headers=["Content-Type", "Authorization"],
)

# Add JWT authentication middleware
# This must be added AFTER CORS middleware to ensure CORS headers are set
app.add_middleware(JWTAuthMiddleware)

# Include routers
app.include_router(auth.router)  # Auth router already has /api/auth prefix
app.include_router(tasks.router, prefix="/api", tags=["tasks"])
app.include_router(chat.router)  # Chat router already has /api prefix


@app.get("/", tags=["root"])
def read_root():
    """Root endpoint returning welcome message.

    Returns:
        Welcome message with API information
    """
    return {
        "message": "Welcome to FastAPI Todo REST API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health"
    }


@app.get("/health", tags=["health"])
def health_check():
    """Health check endpoint for monitoring and load balancers.

    Returns:
        Health status
    """
    return {"status": "healthy"}
