"""Test utilities and helper functions for the Library Platform test suite."""

import json
import uuid
from typing import Any, Dict, List
from datetime import datetime, timezone

import pytest
from fastapi.testclient import TestClient


class DataFactory:
    """Factory class for creating test data."""
    
    @staticmethod
    def create_author_data(
        email: str = None,
        password: str = None,
        name: str = None,
        biography: str = None,
        birth_year: int = None,
        nationality: str = None,
        **kwargs
    ) -> Dict[str, Any]:
        """Create author data for testing."""
        return {
            "email": email or f"test_{uuid.uuid4().hex[:8]}@example.com",
            "password": password or "TestPass123!",
            "name": name or f"Test Author {uuid.uuid4().hex[:4]}",
            "biography": biography or "A test author for unit testing purposes",
            "birth_year": birth_year or 1990,
            "nationality": nationality or "Test Country",
            **kwargs
        }
    
    @staticmethod
    def create_book_data(
        title: str = None,
        genre: str = "FICTION",
        language: str = "ENGLISH",
        published_year: int = None,
        **kwargs
    ) -> Dict[str, Any]:
        """Create book data for testing."""
        return {
            "title": title or f"Test Book {uuid.uuid4().hex[:4]}",
            "genre": genre,
            "language": language,
            "published_year": published_year or 2020,
            **kwargs
        }
    
    @staticmethod
    def create_multiple_authors(count: int) -> List[Dict[str, Any]]:
        """Create multiple author data entries."""
        return [TestDataFactory.create_author_data() for _ in range(count)]
    
    @staticmethod
    def create_multiple_books(count: int, author_id: int = None) -> List[Dict[str, Any]]:
        """Create multiple book data entries."""
        books = []
        for i in range(count):
            book_data = TestDataFactory.create_book_data()
            if author_id:
                book_data["author_id"] = author_id
            books.append(book_data)
        return books


class CSVGenerator:
    """Utility class for generating CSV test data."""
    
    @staticmethod
    def create_books_csv(books_data: List[Dict[str, Any]]) -> str:
        """Create CSV content from books data."""
        if not books_data:
            return "title,genre,language,published_year\n"
        
        csv_lines = ["title,genre,language,published_year"]
        for book in books_data:
            csv_lines.append(f"{book['title']},{book['genre']},{book['language']},{book['published_year']}")
        
        return "\n".join(csv_lines)
    
    @staticmethod
    def create_invalid_csv() -> str:
        """Create invalid CSV content for testing error handling."""
        return "invalid,csv,format\nwithout,proper,headers"
    
    @staticmethod
    def create_csv_with_invalid_data() -> str:
        """Create CSV with invalid book data."""
        return """title,genre,language,published_year
Invalid Book,INVALID_GENRE,ENGLISH,2020
Another Book,FICTION,INVALID_LANGUAGE,2021"""


class JSONGenerator:
    """Utility class for generating JSON test data."""
    
    @staticmethod
    def create_books_json(books_data: List[Dict[str, Any]]) -> str:
        """Create JSON content from books data."""
        return json.dumps(books_data, indent=2)
    
    @staticmethod
    def create_invalid_json() -> str:
        """Create invalid JSON content for testing error handling."""
        return '{"invalid": "json", "missing": "closing bracket"'
    
    @staticmethod
    def create_json_with_invalid_data() -> str:
        """Create JSON with invalid book data."""
        invalid_data = [
            {
                "title": "Invalid Book",
                "genre": "INVALID_GENRE",
                "language": "ENGLISH",
                "published_year": 2020
            }
        ]
        return json.dumps(invalid_data)


class ClientHelper:
    """Helper class for TestClient operations."""
    
    def __init__(self, test_client: TestClient):
        self.client = test_client
    
    def create_author_and_login(self, author_data: Dict[str, Any] = None) -> Dict[str, str]:
        """Create an author and return authentication headers."""
        if author_data is None:
            author_data = TestDataFactory.create_author_data()
        
        # Create author
        response = self.client.post("/api/v1/author/", json=author_data)
        assert response.status_code == 201
        
        # Login
        login_data = {
            "username": author_data["email"],
            "password": author_data["password"]
        }
        response = self.client.post("/api/v1/auth/login", data=login_data)
        assert response.status_code == 200
        
        token = response.json()["access_token"]
        return {"Authorization": f"Bearer {token}"}
    
    def create_author_with_books(self, book_count: int = 3) -> tuple[Dict[str, str], List[int]]:
        """Create an author with books and return auth headers and book IDs."""
        author_data = TestDataFactory.create_author_data()
        auth_headers = self.create_author_and_login(author_data)
        
        book_ids = []
        for i in range(book_count):
            book_data = TestDataFactory.create_book_data(title=f"Book {i+1}")
            response = self.client.post("/api/v1/books/", json=book_data, headers=auth_headers)
            assert response.status_code == 201
            book_ids.append(response.json()["id"])
        
        return auth_headers, book_ids
    
    def create_multiple_authors_with_books(self, author_count: int = 2, books_per_author: int = 2) -> List[Dict[str, Any]]:
        """Create multiple authors with books."""
        authors_data = []
        
        for i in range(author_count):
            author_data = TestDataFactory.create_author_data(name=f"Author {i+1}")
            auth_headers = self.create_author_and_login(author_data)
            
            author_info = {
                "data": author_data,
                "headers": auth_headers,
                "book_ids": []
            }
            
            for j in range(books_per_author):
                book_data = TestDataFactory.create_book_data(title=f"Book {i+1}-{j+1}")
                response = self.client.post("/api/v1/books/", json=book_data, headers=auth_headers)
                assert response.status_code == 201
                author_info["book_ids"].append(response.json()["id"])
            
            authors_data.append(author_info)
        
        return authors_data


class Assertions:
    """Custom assertion helpers for tests."""
    
    @staticmethod
    def assert_valid_token_response(response_data: Dict[str, Any]) -> None:
        """Assert that token response has valid structure."""
        assert "access_token" in response_data
        assert "refresh_token" in response_data
        assert response_data.get("token_type") == "Bearer"
        assert len(response_data["access_token"]) > 0
        assert len(response_data["refresh_token"]) > 0
    
    @staticmethod
    def assert_valid_author_response(response_data: Dict[str, Any]) -> None:
        """Assert that author response has valid structure."""
        required_fields = ["email", "name", "biography", "birth_year", "nationality"]
        for field in required_fields:
            assert field in response_data
        
        assert isinstance(response_data["email"], str)
        assert isinstance(response_data["name"], str)
        assert isinstance(response_data["biography"], str)
        assert isinstance(response_data["birth_year"], int)
        assert isinstance(response_data["nationality"], str)
    
    @staticmethod
    def assert_valid_book_response(response_data: Dict[str, Any]) -> None:
        """Assert that book response has valid structure."""
        required_fields = ["id", "title", "genre", "language", "published_year"]
        for field in required_fields:
            assert field in response_data
        
        assert isinstance(response_data["id"], int)
        assert isinstance(response_data["title"], str)
        assert isinstance(response_data["genre"], str)
        assert isinstance(response_data["language"], str)
        assert isinstance(response_data["published_year"], int)
    
    @staticmethod
    def assert_valid_books_list_response(response_data: Dict[str, Any]) -> None:
        """Assert that books list response has valid structure."""
        assert "items" in response_data
        assert "next_cursor" in response_data
        assert isinstance(response_data["items"], list)
        assert response_data["next_cursor"] is None or isinstance(response_data["next_cursor"], int)
    
    @staticmethod
    def assert_valid_import_response(response_data: Dict[str, Any]) -> None:
        """Assert that import response has valid structure."""
        assert "imported" in response_data
        assert "book_ids" in response_data
        assert isinstance(response_data["imported"], int)
        assert isinstance(response_data["book_ids"], list)
        assert response_data["imported"] >= 0
        assert len(response_data["book_ids"]) == response_data["imported"]


class ErrorChecker:
    """Utility class for checking error responses."""
    
    @staticmethod
    def assert_validation_error(response, field_name: str = None) -> None:
        """Assert that response is a validation error."""
        assert response.status_code == 422
        error_data = response.json()
        assert "detail" in error_data
        
        if field_name:
            error_str = str(error_data)
            assert field_name.lower() in error_str.lower()
    
    @staticmethod
    def assert_unauthorized_error(response) -> None:
        """Assert that response is an unauthorized error."""
        assert response.status_code == 401
    
    @staticmethod
    def assert_not_found_error(response) -> None:
        """Assert that response is a not found error."""
        assert response.status_code == 404
    
    @staticmethod
    def assert_forbidden_error(response) -> None:
        """Assert that response is a forbidden error."""
        assert response.status_code == 403
    
    @staticmethod
    def assert_bad_request_error(response) -> None:
        """Assert that response is a bad request error."""
        assert response.status_code == 400


# Pytest fixtures that can be reused across test files
@pytest.fixture
def test_data_factory():
    """Provide DataFactory instance."""
    return DataFactory()


@pytest.fixture
def test_csv_generator():
    """Provide CSVGenerator instance."""
    return CSVGenerator()


@pytest.fixture
def test_json_generator():
    """Provide JSONGenerator instance."""
    return JSONGenerator()


@pytest.fixture
def test_client_helper(test_client):
    """Provide ClientHelper instance."""
    return ClientHelper(test_client)


@pytest.fixture
def test_assertions():
    """Provide Assertions instance."""
    return Assertions()


@pytest.fixture
def test_error_checker():
    """Provide ErrorChecker instance."""
    return ErrorChecker()


# Additional test data fixtures
@pytest.fixture
def sample_authors_data(test_data_factory):
    """Provide sample authors data."""
    return test_data_factory.create_multiple_authors(3)


@pytest.fixture
def sample_books_data(test_data_factory):
    """Provide sample books data."""
    return test_data_factory.create_multiple_books(5)


@pytest.fixture
def invalid_author_data():
    """Provide invalid author data for testing validation."""
    return {
        "email": "invalid-email",
        "password": "weak",
        "name": "A",  # Too short
        "biography": "Short",  # Too short
        "birth_year": 1700,  # Too old
        "nationality": "A"  # Too short
    }


@pytest.fixture
def invalid_book_data():
    """Provide invalid book data for testing validation."""
    return {
        "title": "",  # Empty
        "genre": "INVALID_GENRE",
        "language": "INVALID_LANGUAGE",
        "published_year": 1700  # Too old
    }
