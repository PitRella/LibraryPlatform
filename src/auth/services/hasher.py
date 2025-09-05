from passlib.context import CryptContext


class Hasher:
    _crypt_context: CryptContext = CryptContext(
        schemes=['bcrypt'],
        deprecated='auto',
    )

    @classmethod
    def hash_password(cls: type['Hasher'], unhashed_password: str) -> str:
        return cls._crypt_context.hash(unhashed_password)

    @classmethod
    def verify_password(
        cls: type['Hasher'],
        unhashed_password: str,
        hashed_password: str,
    ) -> bool:
        return cls._crypt_context.verify(unhashed_password, hashed_password)
