import asyncio
import os
import tempfile
from typing import AsyncGenerator, Generator
from unittest.mock import AsyncMock

import pytest
import pytest_asyncio
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.pool import StaticPool

from src.database import Base
from src.main import app
from src.settings import Settings


@pytest.fixture(scope="session")
def event_loop() -> Generator[asyncio.AbstractEventLoop, None, None]:
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
async def test_engine():
    """Create test database engine."""
    # Use in-memory SQLite for tests
    engine = create_async_engine(
        "sqlite+aiosqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
        echo=False,
    )
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    yield engine
    
    await engine.dispose()


@pytest.fixture
async def test_session(test_engine) -> AsyncGenerator[AsyncSession, None]:
    """Create test database session."""
    async_session = async_sessionmaker(
        test_engine, class_=AsyncSession, expire_on_commit=False
    )
    
    session = async_session()
    try:
        # Clean up any existing data before each test
        await session.rollback()
        # Clear all tables
        for table in reversed(Base.metadata.sorted_tables):
            await session.execute(table.delete())
        await session.commit()
        yield session
    finally:
        await session.close()


@pytest_asyncio.fixture
async def test_client(test_session: AsyncSession) -> TestClient:
    """Create test client with dependency overrides."""
    
    # Override the get_db function to use our test session
    from src.database import get_db
    from src.base.dependencies import get_service
    from src.authors.service import AuthorService
    from src.auth.services import AuthService
    from src.books.services.book import BooksService
    
    async def override_get_db():
        yield test_session
    
    def override_get_service(service_type):
        def _get_service():
            print(f"DEBUG: Creating service {service_type} with session type: {type(test_session)}")
            return service_type(db_session=test_session)
        return _get_service
    
    # Clear any existing overrides first
    app.dependency_overrides.clear()
    
    # Override the database dependency
    app.dependency_overrides[get_db] = override_get_db
    
    # Override all service dependencies
    app.dependency_overrides[get_service(AuthorService)] = override_get_service(AuthorService)
    app.dependency_overrides[get_service(AuthService)] = override_get_service(AuthService)
    app.dependency_overrides[get_service(BooksService)] = override_get_service(BooksService)
    
    with TestClient(app) as client:
        yield client
    
    app.dependency_overrides.clear()


@pytest.fixture
def sample_author_data():
    """Sample author data for testing."""
    return {
        "email": "test@example.com",
        "password": "TestPass123!",
        "name": "Test Author",
        "biography": "A test author for unit testing",
        "birth_year": 1990,
        "nationality": "Test Country"
    }


@pytest.fixture
def sample_book_data():
    """Sample book data for testing."""
    return {
        "title": "Test Book",
        "genre": "FICTION",
        "language": "ENGLISH",
        "published_year": 2020
    }


@pytest.fixture
def sample_books_csv():
    """Sample CSV data for import testing."""
    return """title,genre,language,published_year
Book 1,FICTION,ENGLISH,2020
Book 2,SCIENCE,ENGLISH,2021
Book 3,HISTORY,UKRAINIAN,2019"""


@pytest.fixture
def sample_books_json():
    """Sample JSON data for import testing."""
    return [
        {
            "title": "Book 1",
            "genre": "FICTION",
            "language": "ENGLISH",
            "published_year": 2020
        },
        {
            "title": "Book 2",
            "genre": "SCIENCE",
            "language": "ENGLISH",
            "published_year": 2021
        }
    ]


@pytest.fixture
async def created_author(test_session: AsyncSession, sample_author_data):
    """Create a test author in the database."""
    from src.authors.repositories import AuthorRepository
    from src.auth.services.hasher import Hasher
    
    repo = AuthorRepository(test_session)
    author_data = sample_author_data.copy()
    author_data["password"] = Hasher.hash_password(author_data["password"])
    
    author_id = await repo.create_object(author_data)
    return {"id": author_id, **author_data}


@pytest_asyncio.fixture
async def auth_headers(test_client: TestClient, sample_author_data):
    """Get authentication headers for testing."""
    # Create author
    response = test_client.post("/api/v1/author/", json=sample_author_data)
    assert response.status_code == 200
    
    # Login
    login_data = {
        "username": sample_author_data["email"],
        "password": sample_author_data["password"]
    }
    response = test_client.post("/api/v1/auth/login", data=login_data)
    assert response.status_code == 200
    
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


# Import get_db here to avoid circular imports
from src.database import get_db
