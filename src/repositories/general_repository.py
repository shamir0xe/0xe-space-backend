from typing import Optional, Tuple
from pylib_0xe.types.database_types import DatabaseTypes
from pylib_0xe.types.exception_types import ExceptionTypes
from pylib_0xe.decorators.db_session import db_session
from sqlalchemy.orm import Session

from src.models.general import General
from src.repositories.repository import Repository


class GeneralRepository(Repository[General]):
    @db_session(DatabaseTypes.I)
    def read_by_key(
        self, key: str, session: Optional[Session] = None
    ) -> Tuple[General, Session]:
        if not session:
            raise Exception(ExceptionTypes.DB_SESSION_NOT_FOUND)
        entity = session.query(General).filter(General.key == key).one()
        return entity, session
