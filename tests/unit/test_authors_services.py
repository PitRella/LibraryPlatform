import pytest
from unittest.mock import AsyncMock, patch
from datetime import datetime, timezone

from src.authors.service import AuthorService
from src.authors.schemas import CreateAuthorRequestSchema
from src.authors.exceptions import AuthorNotFoundByIdException
from src.auth.services.hasher import Hasher


class TestAuthorService:
    """Test author service functionality."""
    
    @pytest.fixture
    def mock_session(self):
        """Mock database session."""
        return AsyncMock()
    
    @pytest.fixture
    def mock_repo(self):
        """Mock author repository."""
        return AsyncMock()
    
    @pytest.fixture
    def author_service(self, mock_session):
        """Create author service with mocked dependencies."""
        return AuthorService(mock_session)
    
    @pytest.fixture
    def sample_author_schema(self):
        """Sample author creation schema."""
        return CreateAuthorRequestSchema(
            email="test@example.com",
            password="TestPass123!",
            name="Test Author",
            biography="A test author for unit testing",
            birth_year=1990,
            nationality="Test Country"
        )
    
    @pytest.fixture
    def sample_author_data(self):
        """Sample author data from database."""
        return {
            "id": 1,
            "email": "test@example.com",
            "name": "Test Author",
            "biography": "A test author for unit testing",
            "birth_year": 1990,
            "nationality": "Test Country",
            "created_at": datetime.now(timezone.utc)
        }
    
    @pytest.mark.asyncio
    async def test_get_author_by_id_success(self, author_service, sample_author_data):
        """Test successful author retrieval by ID."""
        # Mock the repository instance directly
        author_service._repo = AsyncMock()
        author_service._repo.get_object.return_value = sample_author_data
        
        result = await author_service.get_author_by_id(1)
        
        assert result == sample_author_data
        author_service._repo.get_object.assert_called_once_with(id=1)
    
    @pytest.mark.asyncio
    async def test_get_author_by_id_string(self, author_service, sample_author_data):
        """Test author retrieval by string ID."""
        # Mock the repository instance directly
        author_service._repo = AsyncMock()
        author_service._repo.get_object.return_value = sample_author_data
        
        result = await author_service.get_author_by_id("1")
        
        assert result == sample_author_data
        author_service._repo.get_object.assert_called_once_with(id=1)
    
    @pytest.mark.asyncio
    async def test_get_author_by_id_not_found(self, author_service):
        """Test author retrieval when author doesn't exist."""
        # Mock the repository instance directly
        author_service._repo = AsyncMock()
        author_service._repo.get_object.return_value = None
        
        with pytest.raises(AuthorNotFoundByIdException):
            await author_service.get_author_by_id(999)
    
    @pytest.mark.asyncio
    async def test_create_author_success(self, author_service, sample_author_schema):
        """Test successful author creation."""
        # Mock the repository instance directly
        author_service._repo = AsyncMock()
        author_service._repo.create_object.return_value = 123
        
        with patch('src.authors.service.Hasher') as mock_hasher:
            mock_hasher.hash_password.return_value = "hashed_password"
            
            with patch('src.authors.service.dt') as mock_dt:
                mock_now = datetime.now(timezone.utc)
                mock_dt.now.return_value = mock_now
                
                result = await author_service.create_author(sample_author_schema)
                
                assert result == 123
                author_service._repo.create_object.assert_called_once()
                
                # Verify the data passed to repository
                call_args = author_service._repo.create_object.call_args[0][0]
                assert call_args["email"] == "test@example.com"
                assert call_args["password"] == "hashed_password"
                assert call_args["name"] == "Test Author"
                assert call_args["biography"] == "A test author for unit testing"
                assert call_args["birth_year"] == 1990
                assert call_args["nationality"] == "Test Country"
                assert call_args["created_at"] == mock_now
    
    @pytest.mark.asyncio
    async def test_create_author_minimal_data(self, author_service):
        """Test author creation with minimal required data."""
        minimal_schema = CreateAuthorRequestSchema(
            email="minimal@example.com",
            password="TestPass123!",
            name="Minimal Author"
        )
        
        # Mock the repository instance directly
        author_service._repo = AsyncMock()
        author_service._repo.create_object.return_value = 456
        
        with patch('src.authors.service.Hasher') as mock_hasher:
            mock_hasher.hash_password.return_value = "hashed_password"
            
            with patch('src.authors.service.dt') as mock_dt:
                mock_now = datetime.now(timezone.utc)
                mock_dt.now.return_value = mock_now
                
                result = await author_service.create_author(minimal_schema)
                
                assert result == 456
                author_service._repo.create_object.assert_called_once()
                
                # Verify the data passed to repository
                call_args = author_service._repo.create_object.call_args[0][0]
                assert call_args["email"] == "minimal@example.com"
                assert call_args["password"] == "hashed_password"
                assert call_args["name"] == "Minimal Author"
                assert call_args["biography"] is None
                assert call_args["birth_year"] is None
                assert call_args["nationality"] is None
                assert call_args["created_at"] == mock_now
    
    @pytest.mark.asyncio
    async def test_create_author_password_hashing(self, author_service):
        """Test that password is properly hashed during creation."""
        schema = CreateAuthorRequestSchema(
            email="test@example.com",
            password="OriginalPassword123!",
            name="Test Author"
        )
        
        # Mock the repository instance directly
        author_service._repo = AsyncMock()
        author_service._repo.create_object.return_value = 789
        
        with patch('src.authors.service.Hasher') as mock_hasher:
            mock_hasher.hash_password.return_value = "hashed_original_password"
            
            with patch('src.authors.service.dt') as mock_dt:
                mock_dt.now.return_value = datetime.now(timezone.utc)
                
                await author_service.create_author(schema)
                
                # Verify password was hashed
                mock_hasher.hash_password.assert_called_once_with("OriginalPassword123!")
                
                # Verify hashed password was stored
                call_args = author_service._repo.create_object.call_args[0][0]
                assert call_args["password"] == "hashed_original_password"
    
    @pytest.mark.asyncio
    async def test_create_author_timestamp_set(self, author_service, sample_author_schema):
        """Test that creation timestamp is properly set."""
        # Mock the repository instance directly
        author_service._repo = AsyncMock()
        author_service._repo.create_object.return_value = 101
        
        with patch('src.authors.service.Hasher') as mock_hasher:
            mock_hasher.hash_password.return_value = "hashed_password"
            
            with patch('src.authors.service.dt') as mock_dt:
                expected_time = datetime.now(timezone.utc)
                mock_dt.now.return_value = expected_time
                
                await author_service.create_author(sample_author_schema)
                
                # Verify timestamp was set
                mock_dt.now.assert_called_once_with(timezone.utc)
                
                call_args = author_service._repo.create_object.call_args[0][0]
                assert call_args["created_at"] == expected_time
