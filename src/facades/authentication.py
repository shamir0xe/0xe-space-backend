from datetime import UTC, datetime
from fastapi import HTTPException, Request
from pylib_0xe.database.actions.release_session import ReleaseSession
from pylib_0xe.database.mediators.engine_mediator import DatabaseTypes

from src.actions.auth.check_token_expired import CheckTokenExpired
from src.models.token import Token
from src.repositories.repository import Repository
from src.models.user import User
from src.types.exception_types import ExceptionTypes


class Authentication:
    def get_user(self, request: Request) -> User:
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            raise HTTPException(401, ExceptionTypes.AUTH_HEADER_INVALID.value)
        token_id = auth_header.split(" ")[1]
        session = None
        try:
            token, session = Repository(Token).read_by_id(
                token_id, db_session_keep_alive=True
            )
        except Exception:
            if session:
                ReleaseSession(DatabaseTypes.I, session).release()
            raise HTTPException(401, "Invalid token")

        if CheckTokenExpired(token).check():
            ReleaseSession(DatabaseTypes.I, session).release()
            raise HTTPException(401, "Token expired")
        # Refresh the token everytime user interacts with proper credentials
        token.updated_at = datetime.now(UTC)
        token, session = Repository(Token).update(token, session=session)
        user = token.user
        session.commit()
        ReleaseSession(DatabaseTypes.I, session).release()
        return user
