import bcrypt


class PasswordFacade:
    @staticmethod
    def hash(plain_password: str) -> bytes:
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(plain_password.encode("utf-8"), salt)
        return hashed

    @staticmethod
    def verify_password(plain_password: str, hashed_password: bytes) -> bool:
        return bcrypt.checkpw(plain_password.encode("utf-8"), hashed_password)
