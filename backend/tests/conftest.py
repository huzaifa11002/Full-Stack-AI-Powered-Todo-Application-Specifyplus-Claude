"""Pytest fixtures for FastAPI Todo API tests.

This module provides shared fixtures for:
- Database setup with SQLite in-memory for testing
- Test client with FastAPI TestClient
- Test users and authentication tokens
- Mock data generators
"""

import os
import pytest
from typing import Generator, Dict, Any
from datetime import datetime, timedelta
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool
from fastapi.testclient import TestClient
from faker import Faker

from app.main import app
from app.database import get_session
from app.models import User, Task
from app.utils.jwt import create_access_token
from app.utils.password import hash_password

# Initialize Faker for generating test data
fake = Faker()

# Set test environment variable
os.environ["TESTING"] = "1"


@pytest.fixture(name="engine")
def engine_fixture():
    """Create an in-memory SQLite database engine for testing.

    Uses StaticPool to ensure the same connection is reused,
    which is necessary for in-memory SQLite databases.
    """
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(engine)
    return engine


@pytest.fixture(name="session")
def session_fixture(engine) -> Generator[Session, None, None]:
    """Create a database session for testing.

    Yields a session and rolls back all changes after the test.
    """
    with Session(engine) as session:
        yield session
        session.rollback()


@pytest.fixture(name="client")
def client_fixture(session: Session) -> Generator[TestClient, None, None]:
    """Create a FastAPI test client with database session override.

    Overrides the get_session dependency to use the test database.
    """
    def get_session_override():
        return session

    app.dependency_overrides[get_session] = get_session_override

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()


@pytest.fixture(name="test_user_data")
def test_user_data_fixture() -> Dict[str, Any]:
    """Generate test user registration data.

    Returns a dictionary with email, password, and username.
    """
    return {
        "email": fake.email().lower(),
        "password": "TestPass123",
        "username": fake.name(),
    }


@pytest.fixture(name="test_user")
def test_user_fixture(session: Session) -> User:
    """Create a test user in the database.

    Returns a User instance with hashed password.
    Password is "TestPass123" (short, under bcrypt 72-byte limit).
    """
    # Use short, fixed password to avoid bcrypt 72-byte limit
    password = "TestPass123"
    user = User(
        email=fake.email().lower(),
        hashed_password=hash_password(password),
        username=fake.name()[:50],  # Limit username length
        is_active=True,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
    )
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


@pytest.fixture(name="test_user_2")
def test_user_2_fixture(session: Session) -> User:
    """Create a second test user for user isolation tests.

    Returns a User instance with hashed password.
    Password is "TestPass456" (short, under bcrypt 72-byte limit).
    """
    # Use short, fixed password to avoid bcrypt 72-byte limit
    password = "TestPass456"
    user = User(
        email=fake.email().lower(),
        hashed_password=hash_password(password),
        username=fake.name()[:50],  # Limit username length
        is_active=True,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
    )
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


@pytest.fixture(name="inactive_user")
def inactive_user_fixture(session: Session) -> User:
    """Create an inactive test user for testing account status checks.

    Returns a User instance with is_active=False.
    Password is "TestPass789" (short, under bcrypt 72-byte limit).
    """
    # Use short, fixed password to avoid bcrypt 72-byte limit
    password = "TestPass789"
    user = User(
        email=fake.email().lower(),
        hashed_password=hash_password(password),
        username=fake.name()[:50],  # Limit username length
        is_active=False,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
    )
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


@pytest.fixture(name="auth_token")
def auth_token_fixture(test_user: User) -> str:
    """Generate a valid JWT token for the test user.

    Returns a JWT token string.
    """
    return create_access_token(user_id=test_user.id, email=test_user.email)


@pytest.fixture(name="auth_token_2")
def auth_token_2_fixture(test_user_2: User) -> str:
    """Generate a valid JWT token for the second test user.

    Returns a JWT token string.
    """
    return create_access_token(user_id=test_user_2.id, email=test_user_2.email)


@pytest.fixture(name="expired_token")
def expired_token_fixture(test_user: User) -> str:
    """Generate an expired JWT token for testing token expiration.

    Returns an expired JWT token string.
    """
    import jwt
    from app.utils.jwt import BETTER_AUTH_SECRET, ALGORITHM

    expire = datetime.utcnow() - timedelta(days=1)  # Expired 1 day ago
    payload = {
        "user_id": test_user.id,
        "email": test_user.email,
        "exp": expire,
        "iat": datetime.utcnow() - timedelta(days=2),
    }
    return jwt.encode(payload, BETTER_AUTH_SECRET, algorithm=ALGORITHM)


@pytest.fixture(name="invalid_token")
def invalid_token_fixture() -> str:
    """Generate an invalid JWT token for testing token validation.

    Returns an invalid JWT token string.
    """
    return "invalid.jwt.token"


@pytest.fixture(name="auth_headers")
def auth_headers_fixture(auth_token: str) -> Dict[str, str]:
    """Generate authorization headers with Bearer token.

    Returns a dictionary with Authorization header.
    """
    return {"Authorization": f"Bearer {auth_token}"}


@pytest.fixture(name="auth_headers_2")
def auth_headers_2_fixture(auth_token_2: str) -> Dict[str, str]:
    """Generate authorization headers for the second test user.

    Returns a dictionary with Authorization header.
    """
    return {"Authorization": f"Bearer {auth_token_2}"}


@pytest.fixture(name="test_task")
def test_task_fixture(session: Session, test_user: User) -> Task:
    """Create a test task for the test user.

    Returns a Task instance.
    """
    task = Task(
        user_id=test_user.id,
        title="Test Task",
        description="This is a test task",
        is_completed=False,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
    )
    session.add(task)
    session.commit()
    session.refresh(task)
    return task


@pytest.fixture(name="test_task_2")
def test_task_2_fixture(session: Session, test_user_2: User) -> Task:
    """Create a test task for the second test user.

    Returns a Task instance.
    """
    task = Task(
        user_id=test_user_2.id,
        title="Test Task for User 2",
        description="This task belongs to user 2",
        is_completed=False,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
    )
    session.add(task)
    session.commit()
    session.refresh(task)
    return task


@pytest.fixture(name="task_data")
def task_data_fixture() -> Dict[str, Any]:
    """Generate test task creation data.

    Returns a dictionary with title and description.
    """
    return {
        "title": fake.sentence(nb_words=5)[:200],  # Limit to 200 chars
        "description": fake.text(max_nb_chars=200),
    }
