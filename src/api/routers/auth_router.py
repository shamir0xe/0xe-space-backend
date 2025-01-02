import logging
from contextlib import asynccontextmanager
from typing import Optional
from fastapi import APIRouter, FastAPI, HTTPException, Request
from pylib_0xe.database.actions.release_session import ReleaseSession
from pylib_0xe.database.mediators.engine_mediator import DatabaseTypes

from src.actions.auth.check_token_expired import CheckTokenExpired
from src.facades.password_facade import PasswordFacade
from src.models.token import Token
from src.repositories.user_repository import UserRepository
from src.repositories.repository import Repository
from src.decorators.auth import auth
from src.models.user import User
from src.types.exception_types import ExceptionTypes
from src.types.api.masked_user import MaskedUser


LOGGER = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # initialize
    # LOGGER.info(f"in the lifespan of the general router")
    yield
    # cleanup
    # LOGGER.info(f"Cleanup")


router = APIRouter(
    prefix=f"/auth",
    tags=["auth"],
    lifespan=lifespan,
)


@router.post("/login")
async def login(username: str, password: str) -> str:
    user, session = UserRepository(User).read_by_username(
        username, db_session_keep_alive=True
    )
    if PasswordFacade.verify_password(password, user.password):
        if not user.token or CheckTokenExpired(user.token).check():
            user.token = Token()
            session.add(user)
        # user, session = Repository(User).update(entity=user, session=session)
    else:
        ReleaseSession(DatabaseTypes.I, session).release()
        raise HTTPException(401, "Username and password do not match")
    session.commit()
    ReleaseSession(DatabaseTypes.I, session).release()
    return user.token.id


@router.get("/logout")
@auth()
async def logout(request: Request, user_id: Optional[str] = None) -> MaskedUser:
    if not user_id:
        raise HTTPException(401, ExceptionTypes.AUTH_REQUIRED.value)
    user, session = Repository(User).read_by_id(user_id, db_session_keep_alive=True)
    if user.token:
        session.delete(user.token)
        session.commit()
    ReleaseSession(DatabaseTypes.I, session).release()
    return MaskedUser(**user.to_dict())
