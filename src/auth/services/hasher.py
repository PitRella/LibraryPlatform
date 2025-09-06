from passlib.context import CryptContext


class Hasher:
    """Utility class for hashing and verifying passwords using bcrypt."""

    _crypt_context: CryptContext = CryptContext(
        schemes=['bcrypt'],
        deprecated='auto',
    )

    @classmethod
    def hash_password(cls: type['Hasher'], unhashed_password: str) -> str:
        """Hash a plain text password.

        Args:
            unhashed_password (str): The plain text password to hash.

        Returns:
            str: The hashed password.

        """
        return cls._crypt_context.hash(unhashed_password)

    @classmethod
    def verify_password(
        cls: type['Hasher'],
        unhashed_password: str,
        hashed_password: str,
    ) -> bool:
        """Verify a plain text password against a hashed password.

        Args:
            unhashed_password (str): The plain text password to verify.
            hashed_password (str): The previously hashed password.

        Returns:
            bool: True if the password matches the hash, False otherwise.

        """
        return cls._crypt_context.verify(unhashed_password, hashed_password)
