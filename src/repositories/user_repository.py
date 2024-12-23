from typing import Optional, Tuple

from pylib_0xe.decorators.db_session import db_session
from pylib_0xe.types.database_types import DatabaseTypes
from sqlalchemy.orm import Session
from pylib_0xe.types.exception_types import ExceptionTypes as Ex0xe
from src.models.user import User
from src.repositories.repository import Repository
from src.types.exception_types import ExceptionTypes


class UserRepository(Repository[User]):
    @db_session(DatabaseTypes.I)
    def read_by_username(
        self, username: str, session: Optional[Session] = None, *args, **kwargs
    ) -> Tuple[User, Session]:
        if not session:
            raise Exception(Ex0xe.DB_SESSION_NOT_FOUND)
        model = session.query(User).filter(User.username == username).first()
        if not model:
            raise Exception(ExceptionTypes.USERNAME_NOT_FOUND)
        return model, session
