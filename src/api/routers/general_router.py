import logging
from contextlib import asynccontextmanager
from typing import Optional
from fastapi import APIRouter, Body, FastAPI, HTTPException, Request
from pylib_0xe.types.database_types import DatabaseTypes
from pylib_0xe.database.actions.release_session import ReleaseSession

from src.repositories.general_repository import GeneralRepository
from src.repositories.repository import Repository
from src.decorators.auth import auth
from src.models.general import General
from src.models.user import User
from src.types.user_roles import UserRoles
from src.types.exception_types import ExceptionTypes


LOGGER = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # initialize
    LOGGER.info(f"in the lifespan of the general router")
    yield
    # cleanup
    LOGGER.info(f"Cleanup")


router = APIRouter(
    prefix=f"/general",
    tags=["general"],
    lifespan=lifespan,
)


@router.get("/get-key")
async def get_value(key: str) -> str:
    try:
        pair, _ = GeneralRepository(General).read_by_key(key=key)
    except:
        raise HTTPException(400, "There is no pair with the given key")
    return pair.value


@router.post("/set-key")
@auth(UserRoles.ADMIN)
async def set_value(
    key: str, request: Request, user_id: Optional[str] = None, text: str = Body(...)
) -> str:
    if not user_id:
        raise HTTPException(401, ExceptionTypes.AUTH_REQUIRED.value)
    user, session = Repository(User).read_by_id(user_id, db_session_keep_alive=True)
    try:
        key_value = General(key=key, value=text, updated_by=user)
        general, session = Repository(General).create(key_value, session=session)
    except Exception:
        general, _ = GeneralRepository(General).read_by_key(key=key)
        session.add(general)
    general.value = text
    general.updated_by = user
    general, session = Repository(General).update(general, session=session)
    ReleaseSession(DatabaseTypes.I, session).release()
    return general.value
