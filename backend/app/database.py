"""Database engine and session management for FastAPI Todo API.

This module provides:
- SQLModel engine configuration with connection pooling
- Database session dependency for FastAPI endpoints
- Error handling for database connection failures
"""

from sqlmodel import SQLModel, Session, create_engine
from typing import Generator
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get database URL from environment variable
# Support both direct DATABASE_URL and individual connection parameters
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    # Construct DATABASE_URL from individual parameters
    DATABASE_HOST = os.getenv("DATABASE_HOST", "localhost")
    DATABASE_PORT = os.getenv("DATABASE_PORT", "5432")
    DATABASE_NAME = os.getenv("DATABASE_NAME", "todo_db")
    DATABASE_USER = os.getenv("DATABASE_USER", "postgres")
    DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD", "password")
    
    # Build connection string
    DATABASE_URL = f"postgresql://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}"

if not DATABASE_URL:
    raise ValueError(
        "DATABASE_URL environment variable is not set. "
        "Please create a .env file with your Neon PostgreSQL connection string."
    )

# Create SQLModel engine with connection pooling
# Connection pooling is handled automatically by SQLAlchemy
engine = create_engine(
    DATABASE_URL,
    echo=False,  # Set to True for SQL query logging during development
    pool_pre_ping=True,  # Verify connections before using them
    pool_size=5,  # Number of connections to maintain
    max_overflow=10,  # Maximum number of connections to create beyond pool_size
)


def get_session() -> Generator[Session, None, None]:
    """FastAPI dependency that provides a database session.

    Yields:
        Session: SQLModel database session

    Usage:
        @app.get("/endpoint")
        def endpoint(session: Session = Depends(get_session)):
            # Use session here
            pass
    """
    with Session(engine) as session:
        try:
            yield session
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()


def create_db_and_tables():
    """Create all database tables defined in SQLModel models.

    This function should be called during application startup or
    via the init_db.py script.
    """
    SQLModel.metadata.create_all(engine)
