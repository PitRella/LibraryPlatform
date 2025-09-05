"""Secure query builder for raw SQL operations.

This module provides a safe way to build dynamic SQL queries
without risk of SQL injection attacks.
"""

from typing import Any


class SecureQueryBuilder:
    """Secure query builder for dynamic SQL operations.

    Provides methods to safely construct SQL queries with dynamic
    WHERE clauses and other conditions without risk of SQL injection.
    """

    # Whitelist of allowed column names for each table
    ALLOWED_COLUMNS = {
        'books': {
            'id',
            'title',
            'genre',
            'language',
            'published_year',
            'author_id',
            'created_at',
        },
        'authors': {
            'id',
            'email',
            'name',
            'biography',
            'birth_year',
            'nationality',
            'created_at',
            'password',
        },
        'refresh_tokens': {
            'id',
            'author_id',
            'refresh_token',
            'expires_in',
            'created_at',
        },
    }

    # Allowed operators for WHERE conditions
    ALLOWED_OPERATORS = {
        '=',
        '!=',
        '<',
        '>',
        '<=',
        '>=',
        'LIKE',
        'IN',
        'NOT IN',
    }

    @classmethod
    def validate_column(cls, table_name: str, column_name: str) -> str:
        """Validate that a column name is allowed for the given table.

        Args:
            table_name (str): Name of the database table.
            column_name (str): Name of the column to validate.

        Returns:
            str: The validated column name.

        Raises:
            ValueError: If the column is not allowed for the table.

        """
        if table_name not in cls.ALLOWED_COLUMNS:
            raise ValueError(f'Unknown table: {table_name}')

        if column_name not in cls.ALLOWED_COLUMNS[table_name]:
            raise ValueError(
                f"Column '{column_name}' not allowed for table '{table_name}'"
            )

        return column_name

    @classmethod
    def validate_operator(cls, operator: str) -> str:
        """Validate that an operator is allowed.

        Args:
            operator (str): SQL operator to validate.

        Returns:
            str: The validated operator.

        Raises:
            ValueError: If the operator is not allowed.

        """
        if operator.upper() not in cls.ALLOWED_OPERATORS:
            raise ValueError(f"Operator '{operator}' not allowed")

        return operator.upper()

    @classmethod
    def build_where_clause(
        cls,
        table_name: str,
        conditions: list[tuple[str, str, str]],
        params: dict[str, Any],
    ) -> tuple[str, dict[str, Any]]:
        """Build a safe WHERE clause from conditions.

        Args:
            table_name (str): Name of the database table.
            conditions (List[Tuple[str, str, str]]): List of (column, operator, param_name) tuples.
            params (Dict[str, Any]): Parameters dictionary.

        Returns:
            Tuple[str, Dict[str, Any]]: WHERE clause and updated parameters.

        Example:
            conditions = [('title', '=', 'title_param'), ('genre', '=', 'genre_param')]
            params = {'title_param': 'Romeo', 'genre_param': 'FICTION'}
            where_clause, params = builder.build_where_clause('books', conditions, params)
            # Returns: ("title = :title_param AND genre = :genre_param", params)

        """
        if not conditions:
            return 'TRUE', params

        validated_conditions = []
        for column, operator, param_name in conditions:
            # Validate column and operator
            validated_column = cls.validate_column(table_name, column)
            validated_operator = cls.validate_operator(operator)

            # Check that parameter exists
            if param_name not in params:
                raise ValueError(
                    f"Parameter '{param_name}' not found in params"
                )

            validated_conditions.append(
                f'{validated_column} {validated_operator} :{param_name}'
            )

        return ' AND '.join(validated_conditions), params

    @classmethod
    def build_set_clause(
        cls, table_name: str, update_fields: list[str], params: dict[str, Any]
    ) -> tuple[str, dict[str, Any]]:
        """Build a safe SET clause for UPDATE statements.

        Args:
            table_name (str): Name of the database table.
            update_fields (List[str]): List of field names to update.
            params (Dict[str, Any]): Parameters dictionary.

        Returns:
            Tuple[str, Dict[str, Any]]: SET clause and updated parameters.

        """
        if not update_fields:
            raise ValueError('No fields provided for update')

        validated_fields = []
        updated_params = {}

        for field in update_fields:
            # Validate column
            validated_field = cls.validate_column(table_name, field)

            # Check that parameter exists with 'set_' prefix
            param_name = f'set_{field}'
            if param_name not in params:
                raise ValueError(
                    f"Parameter '{param_name}' not found in params"
                )

            validated_fields.append(f'{validated_field} = :{param_name}')
            updated_params[param_name] = params[param_name]

        return ', '.join(validated_fields), updated_params
