from fastapi import Request

from models.user import User


class Authentication:
    def get_user(self, request: Request) -> User:
        pass
