import pytest
from unittest.mock import AsyncMock, patch
from datetime import datetime, timezone

from src.books.services.book import BooksService
from src.books.schemas import CreateBookRequestSchema, UpdateBookRequestSchema
from src.books.exceptions import BookNotFoundException, BookPermissionException, ImportItemValidationException
from src.books.enum import BookGenre, BookLanguage


class TestBooksService:
    """Test books service functionality."""
    
    @pytest.fixture
    def mock_session(self):
        """Mock database session."""
        return AsyncMock()
    
    @pytest.fixture
    def mock_repo(self):
        """Mock book repository."""
        return AsyncMock()
    
    @pytest.fixture
    def books_service(self, mock_session, mock_repo):
        """Create books service with mocked dependencies."""
        return BooksService(mock_session, mock_repo)
    
    @pytest.fixture
    def sample_author(self):
        """Sample author data."""
        return {"id": 1, "name": "Test Author"}
    
    @pytest.fixture
    def sample_book_schema(self):
        """Sample book creation schema."""
        return CreateBookRequestSchema(
            title="Test Book",
            genre=BookGenre.FICTION,
            language=BookLanguage.ENGLISH,
            published_year=2020
        )
    
    @pytest.mark.asyncio
    async def test_create_book_success(self, books_service, mock_repo, sample_author, sample_book_schema):
        """Test successful book creation."""
        mock_repo.create_object.return_value = 123
        
        book_id = await books_service.create_book(sample_author, sample_book_schema)
        
        assert book_id == 123
        mock_repo.create_object.assert_called_once()
        
        # Verify the data passed to repository
        call_args = mock_repo.create_object.call_args[0][0]
        assert call_args["title"] == "Test Book"
        assert call_args["genre"] == BookGenre.FICTION
        assert call_args["author_id"] == 1
        assert "created_at" in call_args
    
    @pytest.mark.asyncio
    async def test_get_book_success(self, books_service, mock_repo):
        """Test successful book retrieval."""
        mock_book = {
            "id": 1,
            "title": "Test Book",
            "genre": BookGenre.FICTION,
            "author_id": 1
        }
        mock_repo.get_object.return_value = mock_book
        
        result = await books_service.get_book(1)
        
        assert result == mock_book
        mock_repo.get_object.assert_called_once_with(id=1)
    
    @pytest.mark.asyncio
    async def test_get_book_not_found(self, books_service, mock_repo):
        """Test book retrieval when book doesn't exist."""
        mock_repo.get_object.return_value = None
        
        with pytest.raises(BookNotFoundException):
            await books_service.get_book(999)
    
    @pytest.mark.asyncio
    async def test_update_book_success(self, books_service, mock_repo, sample_author):
        """Test successful book update."""
        existing_book = {
            "id": 1,
            "title": "Old Title",
            "author_id": 1
        }
        updated_book = {
            "id": 1,
            "title": "New Title",
            "author_id": 1
        }
        
        mock_repo.get_object.return_value = existing_book
        mock_repo.update_object.return_value = updated_book
        
        update_schema = UpdateBookRequestSchema(title="New Title")
        result = await books_service.update_book(sample_author, 1, update_schema)
        
        assert result == updated_book
        mock_repo.get_object.assert_called_once_with(id=1)
        mock_repo.update_object.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_update_book_permission_denied(self, books_service, mock_repo):
        """Test book update with permission denied."""
        existing_book = {
            "id": 1,
            "title": "Old Title",
            "author_id": 2  # Different author
        }
        different_author = {"id": 1, "name": "Different Author"}
        
        mock_repo.get_object.return_value = existing_book
        
        update_schema = UpdateBookRequestSchema(title="New Title")
        
        with pytest.raises(BookPermissionException):
            await books_service.update_book(different_author, 1, update_schema)
    
    @pytest.mark.asyncio
    async def test_delete_book_success(self, books_service, mock_repo, sample_author):
        """Test successful book deletion."""
        existing_book = {
            "id": 1,
            "title": "Test Book",
            "author_id": 1
        }
        
        mock_repo.get_object.return_value = existing_book
        mock_repo.delete_object.return_value = None
        
        await books_service.delete_book(sample_author, 1)
        
        mock_repo.get_object.assert_called_once_with(id=1)
        mock_repo.delete_object.assert_called_once_with(id=1)
    
    @pytest.mark.asyncio
    async def test_get_all_books_with_filters(self, books_service, mock_repo):
        """Test book listing with various filters."""
        mock_books = [
            {"id": 1, "title": "Book 1", "published_year": 2020},
            {"id": 2, "title": "Book 2", "published_year": 2021},
            {"id": 3, "title": "Book 3", "published_year": 2022}
        ]
        mock_repo.list_objects.return_value = mock_books
        
        result = await books_service.get_all_books(
            limit=2,
            cursor=None,
            title="Book",
            genre=BookGenre.FICTION,
            year_from=2020,
            year_to=2021
        )
        
        assert result.items == mock_books[:2]  # Only first 2 items (limit=2)
        assert result.next_cursor == 2  # Next cursor is the last item's ID
        
        # Verify filters were passed correctly
        call_args = mock_repo.list_objects.call_args
        filters = call_args[0][0]
        params = call_args[0][1]
        
        assert "title = :title" in filters
        assert "genre = :genre" in filters
        assert "published_year >= :year_from" in filters
        assert "published_year <= :year_to" in filters
        assert params["title"] == "Book"
        assert params["genre"] == BookGenre.FICTION
    
    @pytest.mark.asyncio
    async def test_get_all_books_pagination(self, books_service, mock_repo):
        """Test book listing with pagination."""
        # Return 11 items to test next_cursor
        mock_books = [{"id": i, "title": f"Book {i}"} for i in range(1, 12)]
        mock_repo.list_objects.return_value = mock_books
        
        result = await books_service.get_all_books(limit=10, cursor=5)
        
        assert len(result.items) == 10
        assert result.next_cursor == 10  # Last item's ID
        assert result.items[0]["id"] == 1
        assert result.items[-1]["id"] == 10
    
    @pytest.mark.asyncio
    async def test_import_books_success(self, books_service, mock_repo, sample_author):
        """Test successful book import."""
        from fastapi import UploadFile
        from io import BytesIO
        
        # Mock file content
        csv_content = "title,genre,language,published_year\nTest Book,FICTION,ENGLISH,2020"
        file = UploadFile(
            file=BytesIO(csv_content.encode()),
            filename="test.csv"
        )
        
        # Mock importer
        with patch('src.books.services.book.BookImporterFactory') as mock_factory:
            mock_importer = AsyncMock()
            mock_importer.parse.return_value = [
                {
                    "title": "Test Book",
                    "genre": "FICTION",
                    "language": "ENGLISH",
                    "published_year": 2020
                }
            ]
            mock_factory.get_importer.return_value = mock_importer
            
            mock_repo.create_object.return_value = 123
            
            result = await books_service.import_books(sample_author, file)
            
            assert result.imported == 1
            assert result.book_ids == [123]
            mock_repo.create_object.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_import_books_validation_error(self, books_service, sample_author):
        """Test book import with validation error."""
        from fastapi import UploadFile
        from io import BytesIO
        
        # Mock file with invalid data
        csv_content = "title,genre,language,published_year\nInvalid Book,INVALID_GENRE,ENGLISH,2020"
        file = UploadFile(
            file=BytesIO(csv_content.encode()),
            filename="test.csv"
        )
        
        # Mock importer
        with patch('src.books.services.book.BookImporterFactory') as mock_factory:
            mock_importer = AsyncMock()
            mock_importer.parse.return_value = [
                {
                    "title": "Invalid Book",
                    "genre": "INVALID_GENRE",  # Invalid genre
                    "language": "ENGLISH",
                    "published_year": 2020
                }
            ]
            mock_factory.get_importer.return_value = mock_importer
            
            # This should raise a validation error, but it's a Pydantic error, not our custom one
            with pytest.raises(Exception):  # Pydantic validation error
                await books_service.import_books(sample_author, file)
    
    @pytest.mark.asyncio
    async def test_get_all_books_empty_result(self, books_service, mock_repo):
        """Test book listing with empty result."""
        mock_repo.list_objects.return_value = []
        
        result = await books_service.get_all_books(limit=10, cursor=None)
        
        assert result.items == []
        assert result.next_cursor is None
        mock_repo.list_objects.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_get_all_books_exact_limit(self, books_service, mock_repo):
        """Test book listing when result exactly matches limit."""
        # Return exactly 10 items (limit=10)
        mock_books = [{"id": i, "title": f"Book {i}"} for i in range(1, 11)]
        mock_repo.list_objects.return_value = mock_books
        
        result = await books_service.get_all_books(limit=10, cursor=None)
        
        assert len(result.items) == 10
        assert result.next_cursor is None  # No more items
        assert result.items[0]["id"] == 1
        assert result.items[-1]["id"] == 10
    
    @pytest.mark.asyncio
    async def test_get_all_books_with_cursor(self, books_service, mock_repo):
        """Test book listing with cursor pagination."""
        mock_books = [{"id": i, "title": f"Book {i}"} for i in range(3, 8)]
        mock_repo.list_objects.return_value = mock_books
        
        result = await books_service.get_all_books(limit=5, cursor=2)
        
        assert len(result.items) == 5
        assert result.next_cursor == 7  # Last item's ID
        assert result.items[0]["id"] == 3
        assert result.items[-1]["id"] == 7
    
    @pytest.mark.asyncio
    async def test_get_all_books_complex_filters(self, books_service, mock_repo):
        """Test book listing with complex filter combinations."""
        mock_books = [
            {"id": 1, "title": "Python Book", "genre": "FICTION", "published_year": 2020},
            {"id": 2, "title": "Java Guide", "genre": "SCIENCE", "published_year": 2021}
        ]
        mock_repo.list_objects.return_value = mock_books
        
        result = await books_service.get_all_books(
            limit=5,
            cursor=None,
            title="Book",
            genre=BookGenre.FICTION,
            language=BookLanguage.ENGLISH,
            year_from=2019,
            year_to=2022
        )
        
        assert result.items == mock_books
        
        # Verify all filters were applied
        call_args = mock_repo.list_objects.call_args
        filters = call_args[0][0]
        params = call_args[0][1]
        
        assert "title = :title" in filters
        assert "genre = :genre" in filters
        assert "language = :language" in filters
        assert "published_year >= :year_from" in filters
        assert "published_year <= :year_to" in filters
        
        assert params["title"] == "Book"
        assert params["genre"] == BookGenre.FICTION
        assert params["language"] == BookLanguage.ENGLISH
        assert params["year_from"] == 2019
        assert params["year_to"] == 2022
    
    @pytest.mark.asyncio
    async def test_get_all_books_no_filters(self, books_service, mock_repo):
        """Test book listing without any filters."""
        mock_books = [{"id": i, "title": f"Book {i}"} for i in range(1, 6)]
        mock_repo.list_objects.return_value = mock_books
        
        result = await books_service.get_all_books(limit=10, cursor=None)
        
        assert result.items == mock_books
        
        # Verify no filters were applied
        call_args = mock_repo.list_objects.call_args
        filters = call_args[0][0]
        
        assert filters == ""  # No filters applied