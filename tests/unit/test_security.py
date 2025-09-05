"""Security tests for SQL injection protection."""

import pytest
from src.base.query_builder import SecureQueryBuilder


class TestSecureQueryBuilder:
    """Test cases for SecureQueryBuilder security features."""

    def test_validate_column_allows_valid_columns(self):
        """Test that valid columns are allowed."""
        # Valid columns for books table
        assert SecureQueryBuilder.validate_column('books', 'title') == 'title'
        assert SecureQueryBuilder.validate_column('books', 'genre') == 'genre'
        assert SecureQueryBuilder.validate_column('books', 'author_id') == 'author_id'

    def test_validate_column_rejects_invalid_columns(self):
        """Test that invalid columns are rejected."""
        with pytest.raises(ValueError, match="Column 'invalid_column' not allowed"):
            SecureQueryBuilder.validate_column('books', 'invalid_column')
        
        with pytest.raises(ValueError, match="Column 'password' not allowed"):
            SecureQueryBuilder.validate_column('books', 'password')  # password not in books table

    def test_validate_column_rejects_unknown_table(self):
        """Test that unknown tables are rejected."""
        with pytest.raises(ValueError, match="Unknown table: unknown_table"):
            SecureQueryBuilder.validate_column('unknown_table', 'title')

    def test_validate_operator_allows_valid_operators(self):
        """Test that valid operators are allowed."""
        valid_operators = ['=', '!=', '<', '>', '<=', '>=', 'LIKE', 'IN', 'NOT IN']
        for op in valid_operators:
            assert SecureQueryBuilder.validate_operator(op) == op.upper()

    def test_validate_operator_rejects_invalid_operators(self):
        """Test that invalid operators are rejected."""
        with pytest.raises(ValueError, match="Operator 'INVALID' not allowed"):
            SecureQueryBuilder.validate_operator('INVALID')
        
        with pytest.raises(ValueError, match="Operator 'DROP' not allowed"):
            SecureQueryBuilder.validate_operator('DROP')

    def test_build_where_clause_safe_conditions(self):
        """Test building safe WHERE clauses."""
        conditions = [
            ('title', '=', 'title_param'),
            ('genre', '=', 'genre_param'),
            ('published_year', '>=', 'year_from')
        ]
        params = {
            'title_param': 'Romeo and Juliet',
            'genre_param': 'FICTION',
            'year_from': 1800
        }
        
        where_clause, safe_params = SecureQueryBuilder.build_where_clause(
            'books', conditions, params
        )
        
        assert where_clause == "title = :title_param AND genre = :genre_param AND published_year >= :year_from"
        assert safe_params == params

    def test_build_where_clause_empty_conditions(self):
        """Test building WHERE clause with empty conditions."""
        where_clause, safe_params = SecureQueryBuilder.build_where_clause(
            'books', [], {}
        )
        
        assert where_clause == "TRUE"
        assert safe_params == {}

    def test_build_where_clause_missing_parameter(self):
        """Test that missing parameters raise ValueError."""
        conditions = [('title', '=', 'missing_param')]
        params = {'other_param': 'value'}
        
        with pytest.raises(ValueError, match="Parameter 'missing_param' not found"):
            SecureQueryBuilder.build_where_clause('books', conditions, params)

    def test_build_where_clause_invalid_column(self):
        """Test that invalid columns raise ValueError."""
        conditions = [('invalid_column', '=', 'param')]
        params = {'param': 'value'}
        
        with pytest.raises(ValueError, match="Column 'invalid_column' not allowed"):
            SecureQueryBuilder.build_where_clause('books', conditions, params)

    def test_build_where_clause_invalid_operator(self):
        """Test that invalid operators raise ValueError."""
        conditions = [('title', 'DROP', 'param')]
        params = {'param': 'value'}
        
        with pytest.raises(ValueError, match="Operator 'DROP' not allowed"):
            SecureQueryBuilder.build_where_clause('books', conditions, params)

    def test_build_set_clause_safe_fields(self):
        """Test building safe SET clauses."""
        update_fields = ['title', 'genre', 'published_year']
        params = {
            'set_title': 'New Title',
            'set_genre': 'FICTION',
            'set_published_year': 2023
        }
        
        set_clause, safe_params = SecureQueryBuilder.build_set_clause(
            'books', update_fields, params
        )
        
        assert set_clause == "title = :set_title, genre = :set_genre, published_year = :set_published_year"
        assert safe_params == params

    def test_build_set_clause_empty_fields(self):
        """Test that empty fields raise ValueError."""
        with pytest.raises(ValueError, match="No fields provided for update"):
            SecureQueryBuilder.build_set_clause('books', [], {})

    def test_build_set_clause_invalid_field(self):
        """Test that invalid fields raise ValueError."""
        update_fields = ['invalid_field']
        params = {'set_invalid_field': 'value'}
        
        with pytest.raises(ValueError, match="Column 'invalid_field' not allowed"):
            SecureQueryBuilder.build_set_clause('books', update_fields, params)

    def test_sql_injection_protection_column_names(self):
        """Test protection against SQL injection in column names."""
        # Попытка SQL-инъекции через имя колонки
        malicious_conditions = [
            ("title'; DROP TABLE books; --", '=', 'param'),
            ("title UNION SELECT * FROM authors --", '=', 'param'),
            ("title; DELETE FROM books; --", '=', 'param')
        ]
        
        for condition in malicious_conditions:
            with pytest.raises(ValueError, match="not allowed for table"):
                SecureQueryBuilder.build_where_clause(
                    'books', [condition], {'param': 'value'}
                )

    def test_sql_injection_protection_operators(self):
        """Test protection against SQL injection in operators."""
        # Попытка SQL-инъекции через оператор
        malicious_conditions = [
            ('title', '; DROP TABLE books; --', 'param'),
            ('title', 'UNION SELECT * FROM authors --', 'param'),
            ('title', '; DELETE FROM books; --', 'param')
        ]
        
        for condition in malicious_conditions:
            with pytest.raises(ValueError, match="not allowed"):
                SecureQueryBuilder.build_where_clause(
                    'books', [condition], {'param': 'value'}
                )

    def test_parameter_values_are_safe(self):
        """Test that parameter values are passed through safely."""
        # Параметры с потенциально опасными значениями должны проходить
        # так как они передаются как параметры, а не конкатенируются
        dangerous_params = {
            'title': "'; DROP TABLE books; --",
            'genre': "FICTION'; DELETE FROM books; --",
            'year': "2023; UPDATE books SET title='HACKED'; --"
        }
        
        conditions = [
            ('title', '=', 'title'),
            ('genre', '=', 'genre'),
            ('published_year', '=', 'year')
        ]
        
        # Это должно работать безопасно, так как значения передаются как параметры
        where_clause, safe_params = SecureQueryBuilder.build_where_clause(
            'books', conditions, dangerous_params
        )
        
        assert where_clause == "title = :title AND genre = :genre AND published_year = :year"
        assert safe_params == dangerous_params


class TestPasswordSecurity:
    """Test password security features."""
    
    def test_password_hashing_salt_uniqueness(self):
        """Test that password hashing produces unique salts."""
        from src.auth.services.hasher import Hasher
        
        password = "TestPassword123!"
        hash1 = Hasher.hash_password(password)
        hash2 = Hasher.hash_password(password)
        
        # Hashes should be different due to unique salts
        assert hash1 != hash2
        
        # But both should verify correctly
        assert Hasher.verify_password(password, hash1)
        assert Hasher.verify_password(password, hash2)
    
    def test_password_hashing_consistency(self):
        """Test that password hashing is consistent."""
        from src.auth.services.hasher import Hasher
        
        password = "TestPassword123!"
        hashed = Hasher.hash_password(password)
        
        # Multiple verifications should work
        for _ in range(10):
            assert Hasher.verify_password(password, hashed)
    
    def test_password_hash_format(self):
        """Test that password hashes follow expected format."""
        from src.auth.services.hasher import Hasher
        
        password = "TestPassword123!"
        hashed = Hasher.hash_password(password)
        
        # Should start with bcrypt identifier
        assert hashed.startswith("$2b$")
        
        # Should have correct length for bcrypt
        assert len(hashed) == 60


class TestTokenSecurity:
    """Test JWT token security features."""
    
    def test_access_token_contains_required_claims(self):
        """Test that access tokens contain required claims."""
        from src.auth.services.token import TokenManager
        
        author_id = 123
        token = TokenManager.generate_access_token(author_id)
        decoded = TokenManager.decode_access_token(token)
        
        # Required claims
        assert "sub" in decoded
        assert "exp" in decoded
        assert decoded["sub"] == str(author_id)
        
        # Expiration should be in the future
        from datetime import datetime, timezone
        current_time = datetime.now(timezone.utc).timestamp()
        assert decoded["exp"] > current_time
    
    def test_access_token_expiration_time(self):
        """Test that access tokens have reasonable expiration time."""
        from src.auth.services.token import TokenManager
        
        author_id = 123
        token = TokenManager.generate_access_token(author_id)
        decoded = TokenManager.decode_access_token(token)
        
        from datetime import datetime, timezone
        current_time = datetime.now(timezone.utc).timestamp()
        expiration_time = decoded["exp"]
        
        # Should expire within reasonable time (e.g., 1 hour)
        time_until_expiry = expiration_time - current_time
        assert 0 < time_until_expiry <= 3600  # 1 hour in seconds
    
    def test_refresh_token_uniqueness(self):
        """Test that refresh tokens are unique."""
        from src.auth.services.token import TokenManager
        
        token1, _ = TokenManager.generate_refresh_token()
        token2, _ = TokenManager.generate_refresh_token()
        
        assert token1 != token2
        assert str(token1) != str(token2)
    
    def test_refresh_token_expiration_time(self):
        """Test that refresh tokens have reasonable expiration time."""
        from src.auth.services.token import TokenManager
        
        token, delta = TokenManager.generate_refresh_token()
        
        # Should have reasonable expiration time
        assert delta.total_seconds() > 0
        assert delta.total_seconds() <= 86400 * 7  # Max 7 days
    
    def test_token_decode_with_wrong_secret(self):
        """Test that tokens can't be decoded with wrong secret."""
        from src.auth.services.token import TokenManager
        
        author_id = 123
        token = TokenManager.generate_access_token(author_id)
        
        # This should raise an exception when trying to decode with wrong secret
        with pytest.raises(Exception):
            import jwt
            jwt.decode(token, "wrong_secret", algorithms=["HS256"])
    
    def test_token_tampering_detection(self):
        """Test that token tampering is detected."""
        from src.auth.services.token import TokenManager
        
        author_id = 123
        token = TokenManager.generate_access_token(author_id)
        
        # Tamper with the token
        tampered_token = token[:-5] + "XXXXX"
        
        with pytest.raises(Exception):
            TokenManager.decode_access_token(tampered_token)


class TestInputValidationSecurity:
    """Test input validation security features."""
    
    def test_email_validation_security(self):
        """Test email validation prevents injection."""
        from src.authors.schemas import CreateAuthorRequestSchema
        
        # Test various malicious email patterns
        malicious_emails = [
            "test@example.com'; DROP TABLE authors; --",
            "test@example.com<script>alert('xss')</script>",
            "test@example.com\0",
            "test@example.com\n",
            "test@example.com\r",
        ]
        
        for email in malicious_emails:
            with pytest.raises(Exception):  # Should fail validation
                CreateAuthorRequestSchema(
                    email=email,
                    password="TestPass123!",
                    name="Test Author"
                )
    
    def test_name_validation_security(self):
        """Test name validation prevents injection."""
        from src.authors.schemas import CreateAuthorRequestSchema
        
        # Test various malicious name patterns
        malicious_names = [
            "<script>alert('xss')</script>",
            "'; DROP TABLE authors; --",
            "Name\0",
            "Name\n",
            "Name\r",
        ]
        
        for name in malicious_names:
            with pytest.raises(Exception):  # Should fail validation
                CreateAuthorRequestSchema(
                    email="test@example.com",
                    password="TestPass123!",
                    name=name
                )
    
    def test_book_title_validation_security(self):
        """Test book title validation prevents injection."""
        from src.books.schemas import CreateBookRequestSchema
        
        # Test various malicious title patterns
        malicious_titles = [
            "<script>alert('xss')</script>",
            "'; DROP TABLE books; --",
            "Title\0",
            "Title\n",
            "Title\r",
        ]
        
        for title in malicious_titles:
            with pytest.raises(Exception):  # Should fail validation
                CreateBookRequestSchema(
                    title=title,
                    genre="FICTION",
                    language="ENGLISH",
                    published_year=2020
                )
